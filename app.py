import io
import math
import random
import sys
import time
import wave
from array import array

import streamlit as st

st.set_page_config(
    page_title="MindCare - Mental Health & Helpline Directory",
    page_icon="🌱",
    layout="wide"
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');

        :root {
            --ink: #203d34;
            --muted: #62756b;
            --forest: #245c4b;
            --forest-deep: #173b32;
            --leaf: #9eb66c;
            --coral: #c66c50;
            --paper: #f3f7f3;
            --surface: #ffffff;
            --line: #dce7df;
        }

        .stApp {
            background: linear-gradient(132deg, #f1f6f1 0%, #fbfaf6 54%, #edf5f2 100%);
            color: var(--ink);
            font-family: 'DM Sans', 'Segoe UI', sans-serif;
        }

        .main .block-container {
            max-width: 1280px;
            padding: 2.5rem 3rem 4rem;
        }

        h1, h2, h3, h4 {
            color: var(--ink);
            font-family: 'Fraunces', Georgia, serif;
            font-weight: 600;
            letter-spacing: 0;
        }

        h1 {
            margin-bottom: 0.35rem;
            font-size: 2.45rem;
            line-height: 1.15;
        }

        h2, h3 {
            line-height: 1.25;
        }

        p, label, [data-testid="stCaptionContainer"] {
            color: var(--muted);
            line-height: 1.65;
        }

        .hero-card {
            background: linear-gradient(118deg, #e3efe5 0%, #f2f5e9 58%, #e8f2ef 100%);
            border: 1px solid #d6e4d9;
            border-left: 5px solid var(--leaf);
            border-radius: 16px;
            padding: 2.4rem 2.6rem;
            box-shadow: 0 16px 38px rgba(31, 68, 52, 0.08);
            margin-bottom: 1.75rem;
        }

        .welcome-message {
            margin: 0 0 0.8rem;
            color: var(--forest);
            font-family: 'Fraunces', Georgia, serif;
            font-size: 2.8rem;
            font-weight: 600;
            line-height: 1.1;
        }

        .reassurance-note {
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
            margin: 1.15rem 0 1.65rem;
            padding: 1rem 1.2rem;
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid var(--line);
            border-left: 4px solid var(--coral);
            border-radius: 10px;
        }

        .reassurance-note .reassurance-icon {
            font-size: 1.35rem;
            line-height: 1.4;
        }

        .reassurance-note strong {
            color: var(--forest-deep);
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.15rem;
        }

        .reassurance-note p {
            margin: 0.15rem 0 0;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .feature-card {
            height: 100%;
            background: var(--surface);
            border: 1px solid var(--line);
            border-top: 3px solid var(--leaf);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 8px 22px rgba(31, 68, 52, 0.045);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 13px 28px rgba(31, 68, 52, 0.09);
        }

        .feature-card h4 {
            color: var(--forest-deep);
            font-size: 1.15rem;
        }

        .feature-card p {
            color: var(--muted) !important;
            font-size: 0.94rem;
        }

        .auth-card {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 18px 45px rgba(31, 68, 52, 0.09);
            max-width: 680px;
        }

        .signup-reassurance {
            margin: 0 0 1.1rem;
            color: var(--forest);
            font-family: 'Fraunces', Georgia, serif;
            font-size: 2.25rem;
            font-weight: 600;
            line-height: 1.15;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(255, 255, 255, 0.12);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(165deg, #173b32 0%, #214d40 100%);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #eef5ed !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 9px;
            padding: 0.38rem 0.55rem;
            transition: background 140ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.09);
        }

        .stButton > button {
            min-height: 2.7rem;
            background: var(--forest);
            color: white;
            border: 1px solid var(--forest);
            border-radius: 10px;
            padding: 0.62rem 1.1rem;
            font-weight: 600;
            transition: background 150ms ease, transform 150ms ease, box-shadow 150ms ease;
            box-shadow: 0 3px 9px rgba(23, 59, 50, 0.12);
        }

        .stButton > button:hover {
            background: var(--forest-deep);
            border-color: var(--forest-deep);
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(23, 59, 50, 0.17);
        }

        .stButton > button p {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: #9e4836;
            border-color: #9e4836;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #7e342a;
            border-color: #7e342a;
        }

        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea,
        [data-baseweb="select"] > div {
            background: #fff;
            border-color: #d2dfd6;
            border-radius: 9px;
        }

        [data-baseweb="input"] input:focus,
        [data-baseweb="textarea"] textarea:focus {
            border-color: var(--forest);
            box-shadow: 0 0 0 2px rgba(36, 92, 75, 0.13);
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--line);
            border-radius: 11px;
            padding: 1rem 1.1rem;
        }

        [data-testid="stMetricValue"] {
            color: var(--forest);
            font-family: 'Fraunces', Georgia, serif;
        }

        [data-testid="stProgress"] > div > div > div {
            background: var(--forest);
        }

        [data-testid="stChatMessage"] {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.78);
        }

        .winddown-timer {
            margin: 1.25rem 0 1.75rem;
            padding: 1.6rem;
            border: 1px solid #d2e1d5;
            border-radius: 14px;
            background: linear-gradient(125deg, #e7f0e7 0%, #f3f3e9 100%);
        }

        .winddown-label {
            color: var(--forest);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .winddown-clock {
            margin: 0.2rem 0;
            color: var(--forest-deep);
            font-family: 'Fraunces', Georgia, serif;
            font-size: 3.2rem;
            line-height: 1.1;
            font-variant-numeric: tabular-nums;
        }

        .winddown-status {
            margin: 0.5rem 0 1rem;
        }

        .winddown-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }

        .winddown-actions button {
            min-height: 2.6rem;
            padding: 0.55rem 0.95rem;
            border: 1px solid var(--forest);
            border-radius: 9px;
            background: var(--forest);
            color: #fff;
            font: inherit;
            font-weight: 600;
            cursor: pointer;
        }

        .winddown-actions button:hover:not(:disabled) {
            background: var(--forest-deep);
        }

        .winddown-actions button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        hr {
            border-color: var(--line);
        }

        @media (max-width: 760px) {
            .main .block-container {
                padding: 1.5rem 1rem 2.5rem;
            }

            h1 {
                font-size: 2rem;
            }

            .hero-card {
                padding: 1.5rem;
            }

            .auth-card {
                padding: 1.25rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- VERIFIED INDIAN HELPLINES DATASET ---
HELPLINES = [
    {
        "name": "Tele-MANAS (Govt. of India)",
        "number": "14416",
        "category": "Crisis / General",
        "timing": "24x7",
        "languages": "Kannada, Hindi, English & all regional languages",
        "desc": "Official toll-free mental health helpline by the Ministry of Health & Family Welfare."
    },
    {
        "name": "KIRAN Mental Health Helpline",
        "number": "1800-599-0019",
        "category": "Crisis / Rehabilitation",
        "timing": "24x7",
        "languages": "Multi-lingual",
        "desc": "Operated by the Ministry of Social Justice and Empowerment for psychological support and distress."
    },
    {
        "name": "Vandrevala Foundation",
        "number": "+91 9999 666 555",
        "category": "Anxiety & Depression",
        "timing": "24x7",
        "languages": "English, Hindi",
        "desc": "Free professional telephonic and WhatsApp mental health counseling."
    },
    {
        "name": "AASRA",
        "number": "+91 98204 66726",
        "category": "Crisis / Suicide Prevention",
        "timing": "24x7",
        "languages": "English, Hindi",
        "desc": "Non-judgmental, confidential 24-hour suicide prevention helpline."
    },
    {
        "name": "Parivarthan Counseling Helpline",
        "number": "+91 7676 602 602",
        "category": "Student / General Stress",
        "timing": "1:00 PM – 10:00 PM (Mon-Fri)",
        "languages": "English, Kannada, Hindi",
        "desc": "Confidential support tailored for academic pressure, stress, and anxiety."
    }
]

def get_companion_reply(prompt: str) -> str:
    message = prompt.strip().lower()
    if not message:
        return "Write a thought or question, and we can take it one step at a time."

    if any(term in message for term in ("suicide", "kill myself", "hurt myself", "self-harm", "end my life")):
        return (
            "I’m sorry things feel this difficult. If you may be in immediate danger, call 112 now "
            "or go to the nearest emergency department. In India, you can also call Tele-MANAS at 14416. "
            "Please reach out to someone you trust and stay with them."
        )
    if any(term in message for term in ("anxious", "anxiety", "panic", "stressed", "overwhelmed")):
        return (
            "That sounds like a lot to carry. Try one slow breath in, then a longer breath out. "
            "Notice one thing you can see and one small next step that feels manageable."
        )
    if any(term in message for term in ("sad", "lonely", "down", "depressed")):
        return (
            "I’m sorry you’re feeling this way. You deserve support with it. "
            "Could you message someone you trust, or choose one gentle thing to do for yourself right now?"
        )
    if any(term in message for term in ("sleep", "tired", "rest")):
        return (
            "Rest can be hard when your mind is busy. Try dimming your screen, relaxing your shoulders, "
            "and taking a few slow breaths. You don’t have to solve everything tonight."
        )
    return (
        "Thanks for sharing that with me. I can offer a grounding exercise, a breathing reset, "
        "or a journaling prompt. What would feel most helpful right now?"
    )


def create_ambient_audio(soundscape: str, duration_seconds: int) -> bytes:
    sample_rate = 16000
    samples = array("h")
    filtered_noise = 0.0
    brown_noise = 0.0
    sample_count = sample_rate * duration_seconds
    fade_samples = int(sample_rate * 0.15)
    melody_notes = [220.0, 261.63, 293.66, 329.63, 392.0, 440.0, 523.25]
    melody_pattern = [0, 2, 3, 4, 2, 1, 0, 2, 4, 5, 4, 2, 3, 1, 0, 1]
    chord_roots = [110.0, 130.81, 98.0, 110.0]

    for sample_index in range(sample_count):
        white_noise = random.uniform(-1.0, 1.0)
        elapsed = sample_index / sample_rate

        if soundscape == "White noise":
            value = white_noise * 0.22
        elif soundscape == "Pink noise":
            filtered_noise = 0.96 * filtered_noise + 0.04 * white_noise
            value = filtered_noise * 0.55 + white_noise * 0.12
        elif soundscape == "Brown noise":
            brown_noise = (brown_noise + 0.02 * white_noise) / 1.02
            value = brown_noise * 3.0
        elif soundscape == "Gentle rainfall":
            filtered_noise = 0.82 * filtered_noise + 0.18 * white_noise
            value = filtered_noise * 0.3 + white_noise * 0.12
        elif soundscape == "Ocean waves":
            brown_noise = (brown_noise + 0.02 * white_noise) / 1.02
            wave_envelope = 0.12 + 0.88 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.12 * elapsed))
            value = brown_noise * 3.0 * wave_envelope + white_noise * 0.07 * wave_envelope
        elif soundscape == "Running stream":
            filtered_noise = 0.7 * filtered_noise + 0.3 * white_noise
            flow = 0.82 + 0.18 * math.sin(2 * math.pi * 0.18 * elapsed)
            value = (filtered_noise * 0.32 + white_noise * 0.1) * flow
        elif soundscape == "Forest birds":
            filtered_noise = 0.995 * filtered_noise + 0.005 * white_noise
            value = filtered_noise * 0.45 + white_noise * 0.025
            bird_time = elapsed % 3.7
            if bird_time < 0.19:
                chirp_phase = 2 * math.pi * (1900 * bird_time + 0.5 * 6000 * bird_time ** 2)
                chirp_envelope = math.sin(math.pi * bird_time / 0.19) ** 2
                value += math.sin(chirp_phase) * chirp_envelope * 0.13
            elif 0.3 <= bird_time < 0.45:
                chirp_time = bird_time - 0.3
                chirp_phase = 2 * math.pi * (2400 * chirp_time - 0.5 * 3000 * chirp_time ** 2)
                chirp_envelope = math.sin(math.pi * chirp_time / 0.15) ** 2
                value += math.sin(chirp_phase) * chirp_envelope * 0.1
        elif soundscape == "Soft guitar melody":
            note_duration = 0.55
            note_position = int(elapsed / note_duration)
            note_time = elapsed % note_duration
            note_frequency = melody_notes[melody_pattern[note_position % len(melody_pattern)]]
            phase = 2 * math.pi * note_frequency * note_time
            pluck = (
                math.sin(phase) * 0.62
                + math.sin(2 * phase) * 0.25
                + math.sin(3 * phase) * 0.13
                + math.sin(4 * phase) * 0.05
            )
            attack = 1 - math.exp(-note_time * 90)
            decay = math.exp(-note_time * 4.2)
            chord_frequency = chord_roots[(note_position // 4) % len(chord_roots)]
            chord = math.sin(2 * math.pi * chord_frequency * elapsed) * 0.045
            value = pluck * attack * decay * 0.3 + chord
        else:
            value = 0.0

        fade_in = min(1.0, sample_index / fade_samples)
        fade_out = min(1.0, (sample_count - sample_index - 1) / fade_samples)
        value *= min(fade_in, fade_out)
        samples.append(int(max(-0.8, min(0.8, value)) * 32767))

    if sys.byteorder != "little":
        samples.byteswap()

    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(sample_rate)
        audio_file.writeframes(samples.tobytes())
    return audio_buffer.getvalue()


# --- SIDEBAR NAVIGATION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = "Create Free Account"
if "navigation_history" not in st.session_state:
    st.session_state["navigation_history"] = []
if "last_menu" not in st.session_state:
    st.session_state["last_menu"] = None
if "nav_target" in st.session_state:
    st.session_state["selected_menu"] = st.session_state["nav_target"]
    del st.session_state["nav_target"]
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {
            "role": "assistant",
            "content": "Hi, I’m your MindCare companion. I can help with grounding, healthy routines, and stress support. What would you like support with today?",
        }
    ]

if st.session_state["logged_in"]:
    nav_items = [
        "Dashboard",
        "Wellness Companion",
        "Self-Care Journal",
        "Helpline Directory",
        "Quick Mood Check-in",
        "Grounding & Breathing",
        "Daily Affirmation",
        "Sleep Wind-Down",
    ]
else:
    nav_items = ["Create Free Account", "Sign Up", "Login"]

st.sidebar.title("🌱 MindCare Hub")
if st.sidebar.button("⚡ Quick Exit", key="quick_exit", help="Clear this session’s chat and open a neutral page"):
    st.session_state["chat_history"] = []
    st.session_state["navigation_history"] = []
    st.html(
        '<script>window.location.replace("https://www.wikipedia.org/");</script>',
        unsafe_allow_javascript=True,
    )
    st.stop()

menu = st.sidebar.radio(
    "Navigation",
    nav_items,
    key="selected_menu"
)

if menu != st.session_state["last_menu"]:
    previous_menu = st.session_state["last_menu"]
    if (
        st.session_state["logged_in"]
        and previous_menu in nav_items
        and menu in nav_items
        and not st.session_state.pop("skip_navigation_history", False)
    ):
        st.session_state["navigation_history"].append(previous_menu)
    st.session_state["last_menu"] = menu

if st.session_state["logged_in"]:
    if st.sidebar.button("Log out"):
        st.session_state["logged_in"] = False
        st.session_state["navigation_history"] = []
        st.session_state["nav_target"] = "Login"
        st.rerun()

st.sidebar.markdown("---")
with st.sidebar.expander("Trusted emergency contact"):
    guardian_number = st.text_input(
        "Guardian phone number",
        placeholder="+1 555 123 4567",
        key="guardian_phone_number",
        help="Keep a trusted person’s number handy for emergencies.",
    )
    guardian_digits = "".join(character for character in guardian_number if character.isdigit())
    allowed_phone_characters = set("0123456789+ ()-.")
    has_valid_plus = guardian_number.count("+") <= 1 and guardian_number.find("+") <= 0
    if guardian_number:
        if (
            7 <= len(guardian_digits) <= 15
            and all(character in allowed_phone_characters for character in guardian_number)
            and has_valid_plus
        ):
            call_number = f"+{guardian_digits}" if guardian_number.strip().startswith("+") else guardian_digits
            st.link_button("Call guardian", f"tel:{call_number}", use_container_width=True)
        else:
            st.caption("Enter 7–15 digits; spaces, parentheses, hyphens, dots, and a leading + are okay.")
    st.caption("This number stays in the current app session and is not sent anywhere.")
st.sidebar.warning("⚠️ **Immediate Emergency:** Dial **112** or **14416** (Tele-MANAS).")

if st.session_state["logged_in"] and st.session_state["navigation_history"]:
    previous_page = st.session_state["navigation_history"][-1]
    if st.button(f"← Back to {previous_page}", key="back_to_previous_page"):
        st.session_state["navigation_history"].pop()
        st.session_state["skip_navigation_history"] = True
        st.session_state["nav_target"] = previous_page
        st.rerun()

# --- 1. DASHBOARD ---
if menu == "Dashboard":
    st.title("🌿 Your Wellness Dashboard")
    st.caption("A calm place to check in, breathe, and access trusted support.")
    st.markdown(
        """
        <div class="reassurance-note">
            <span class="reassurance-icon">🌼</span>
            <div>
                <strong>You are not alone.</strong>
                <p>Take today one small step at a time. You deserve kindness, and support is here when you need it.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:2rem;">💙</div>
                <h4 style="margin:0.2rem 0;">Daily Calm</h4>
                <p style="margin:0; color:#465a6f;">Grounding exercises to help steady your body and mind.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:2rem;">📊</div>
                <h4 style="margin:0.2rem 0;">Mood Check</h4>
                <p style="margin:0; color:#465a6f;">Track your emotional energy in just a few quick questions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:2rem;">📞</div>
                <h4 style="margin:0.2rem 0;">Support</h4>
                <p style="margin:0; color:#465a6f;">Reach trusted helplines and crisis support when you need it.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("### Today's focus")
        st.write("Take five minutes for yourself. Start with a gentle breath, then check in with your mood and your energy for the day.")
        if st.button("De-stress yourself"):
            st.session_state["nav_target"] = "Grounding & Breathing"
            st.rerun()
        if st.button("Open mood check-in"):
            st.session_state["nav_target"] = "Quick Mood Check-in"
            st.rerun()

    with right:
        st.markdown("### Quick access")
        if st.button("🏠 Dashboard"):
            st.session_state["nav_target"] = "Dashboard"
            st.rerun()
        if st.button("🤖 Wellness Companion"):
            st.session_state["nav_target"] = "Wellness Companion"
            st.rerun()
        if st.button("📞 Helpline Directory"):
            st.session_state["nav_target"] = "Helpline Directory"
            st.rerun()
        if st.button("✨ Daily Affirmation"):
            st.session_state["nav_target"] = "Daily Affirmation"
            st.rerun()

    st.markdown("---")
    st.subheader("Wellness snapshot")
    snapshot = st.columns(3)
    snapshot[0].metric("Support", "24/7")
    snapshot[1].metric("Helplines", str(len(HELPLINES)))
    snapshot[2].metric("Care style", "Gentle")

    st.markdown("---")
    st.subheader("Today’s care plan")
    care_plan = [
        "Drink water and take a 2-minute stretch break",
        "Notice one thought that feels heavy and soften it gently",
        "Take a 5-minute breathing reset before your next task",
    ]
    for item in care_plan:
        st.checkbox(item, value=False, key=f"care_{item[:12]}")

    st.markdown("---")
    st.subheader("Quick actions")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Open Wellness Companion"):
            st.session_state["nav_target"] = "Wellness Companion"
            st.rerun()
    with q2:
        if st.button("Mood check-in"):
            st.session_state["nav_target"] = "Quick Mood Check-in"
            st.rerun()
    with q3:
        if st.button("Helpline directory"):
            st.session_state["nav_target"] = "Helpline Directory"
            st.rerun()

# --- 2. WELLNESS COMPANION ---
elif menu == "Wellness Companion":
    st.title("🤖 MindCare Wellness Companion")
    st.write("A gentle, private space to get quick support, grounding ideas, and reflection prompts.")

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask for support, a calming plan, or a daily check-in prompt...")
    if prompt:
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Thinking..."):
            reply = get_companion_reply(prompt)

        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# --- 3. SELF-CARE JOURNAL ---
elif menu == "Self-Care Journal":
    st.title("📓 Gentle Reflection Journal")
    st.write("Reflect with a few simple prompts to help your mind slow down and become more aware.")

    prompts = [
        "What is one thing that feels heavy right now?",
        "What helped me feel a little calmer today?",
        "What is one small step I can take in the next hour to care for myself?",
    ]

    journal_entry = st.text_area("Write your thoughts here:", height=180, placeholder="I am feeling...")
    if st.button("Save reflection"):
        if journal_entry.strip():
            st.success("Your reflection has been saved in this session.")
            st.session_state["latest_journal"] = journal_entry
        else:
            st.warning("Please write a few words before saving your reflection.")

    st.markdown("---")
    st.subheader("Prompt ideas")
    for prompt in prompts:
        st.info(prompt)

# --- 4. HELPLINE DIRECTORY ---
elif menu == "Helpline Directory":
    st.title("📞 Verified Helpline Directory")
    st.write("Fast, categorized access to toll-free mental health support across India.")

    categories = ["All"] + sorted(list({h["category"] for h in HELPLINES}))
    selected_category = st.selectbox("Filter by Category / Need:", categories)
    search_query = st.text_input("Search helpline by name or focus:", "")

    filtered = HELPLINES
    if selected_category != "All":
        filtered = [h for h in filtered if h["category"] == selected_category]
    if search_query:
        filtered = [h for h in filtered if search_query.lower() in h["name"].lower() or search_query.lower() in h["desc"].lower()]

    st.markdown(f"**Found {len(filtered)} resource(s):**")
    for item in filtered:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(item["name"])
                st.write(item["desc"])
                st.caption(f"🕒 Hours: {item['timing']} | 🌐 Languages: {item['languages']}")
            with col2:
                clean_num = item["number"].replace(" ", "").replace("-", "")
                st.markdown(f"### `{item['number']}`")
                st.markdown(
                    f'<a href="tel:{clean_num}"><button style="width:100%; padding:10px; border-radius:6px; background:#2e7d32; color:white; border:none; font-weight:bold; cursor:pointer;">📞 Call Now</button></a>',
                    unsafe_allow_html=True
                )

# --- 2. LOGIN PAGE ---
elif menu == "Login":
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-top: 1rem;">
            <div class="auth-card">
                <h2 style="margin-top: 0; margin-bottom: 0.5rem;">🔐 Login to MindCare</h2>
                <p style="margin-top: 0; color: #3d5368;">Welcome back. Continue with your email and password.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("Email address", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        remember = st.checkbox("Keep me signed in")
        submit = st.form_submit_button("Login")

    if submit:
        if not email:
            st.warning("Please enter your email address.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.warning("Please enter a valid email address.")
        elif not password:
            st.warning("Please enter your password.")
        else:
            st.session_state["logged_in"] = True
            st.session_state["nav_target"] = "Dashboard"
            st.success(f"Welcome back, {email}!")
            st.info("You are now logged in. Your wellness dashboard is ready.")
            st.balloons()
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

# --- 3. FREE ACCOUNT PAGE ---
elif menu == "Create Free Account":
    st.markdown(
        """
        <div class="hero-card">
            <p class="welcome-message">We’re always here for you.</p>
            <h1 style="margin-bottom: 0.5rem;">✨ Start your free MindCare journey</h1>
            <p style="font-size: 1.1rem; margin-bottom: 0; color: #2d4153;">
                Personalized wellness support, guided calm tools, and trusted mental health resources in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    features = [
        ("🧠", "Mood check-ins", "Daily insight into stress, energy, and emotional balance."),
        ("🌬️", "Breathing tools", "Quick grounding exercises to calm anxiety and reset focus."),
        ("📞", "Verified helplines", "Access trusted crisis and support resources across India."),
        ("🌱", "Daily affirmations", "Positive perspective that helps you begin each day gently."),
    ]
    for col, (icon, title, text) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <h4 style="margin: 0 0 0.5rem 0;">{title}</h4>
                    <p style="margin: 0; color: #465a6f;">{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.info("Your account is free, private, and designed to help you feel supported in under two minutes.")

    if st.button("Create my free account"):
        st.session_state["nav_target"] = "Sign Up"
        st.session_state["signup_email"] = ""
        st.session_state["account_page_redirect"] = True
        st.rerun()

# --- 4. SIGN UP PAGE ---
elif menu == "Sign Up":
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-top: 1rem;">
            <div class="auth-card">
                <p class="signup-reassurance">You are not alone.</p>
                <h2 style="margin-top: 0; margin-bottom: 0.5rem;">📝 Create your MindCare account</h2>
                <p style="margin-top: 0; color: #3d5368;">Sign up with your email to begin your free wellness journey.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("signup_form", clear_on_submit=True):
        email = st.text_input("Email address", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        agree = st.checkbox("I agree to the terms and privacy policy.")
        submit = st.form_submit_button("Create account")

    if submit:
        if not email:
            st.warning("Please enter your email address.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.warning("Please enter a valid email address.")
        elif not password:
            st.warning("Please create a password.")
        elif not agree:
            st.warning("Please accept the terms before continuing.")
        else:
            st.session_state["logged_in"] = True
            st.session_state["nav_target"] = "Dashboard"
            st.success(f"Account ready for {email}!")
            st.info("Your sign-up is complete. Your personalized dashboard is ready.")
            st.balloons()
            st.rerun()

    st.markdown("<div style='margin-top: 1.2rem; display: flex; gap: 0.75rem; flex-wrap: wrap;'>", unsafe_allow_html=True)
    if st.button("Create free account"):
        st.session_state["nav_target"] = "Create Free Account"
        st.rerun()
    if st.button("Sign up"):
        st.session_state["nav_target"] = "Sign Up"
        st.rerun()
    if st.button("Login"):
        st.session_state["nav_target"] = "Login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# --- 5. QUICK MOOD CHECK-IN ---
elif menu == "Quick Mood Check-in":
    st.title("📝 Quick Mood Check-in")
    st.write("Answer the first two questions for the PHQ-2 self-check, then use the extra questions to reflect on your wellbeing. This is not a diagnosis.")

    q1 = st.slider(
        "1. Over the last 2 weeks, how often have you had little interest or pleasure in doing things?",
        0, 3, 0,
        help="0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"
    )

    q2 = st.slider(
        "2. Over the last 2 weeks, how often have you felt down, depressed, or hopeless?",
        0, 3, 0,
        help="0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"
    )

    st.markdown("### A little more about how you’ve been")
    q3 = st.slider(
        "3. Over the last 2 weeks, how often has stress felt difficult to manage?",
        0, 3, 0,
        help="0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"
    )
    q4 = st.slider(
        "4. Over the last 2 weeks, how often has sleep felt difficult or unrefreshing?",
        0, 3, 0,
        help="0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"
    )
    q5 = st.slider(
        "5. Over the last 2 weeks, how often have you felt you had someone you could turn to for support?",
        0, 3, 0,
        help="0 = Never, 1 = Some days, 2 = Most days, 3 = Nearly every day"
    )

    if st.button("Review check-in"):
        total = q1 + q2
        st.markdown("---")
        st.subheader(f"PHQ-2 self-check: {total} / 6")
        st.caption("Only the first two answers are included in this score. The additional questions are for personal reflection.")
        if total < 3:
            st.info("Your PHQ-2 score is below the usual follow-up threshold. If you are still concerned about how you feel, consider talking with someone you trust or a health professional.")
        else:
            st.info("A PHQ-2 score of 3 or more is a reason to consider discussing how you’ve been feeling with a health professional. This result is not a diagnosis.")

        st.markdown("### Your reflection")
        st.write(f"Stress has felt difficult to manage: **{q3} / 3**")
        st.write(f"Sleep has felt difficult or unrefreshing: **{q4} / 3**")
        st.write(f"Feeling able to turn to someone for support: **{q5} / 3**")

# --- 6. GROUNDING & BREATHING ---
elif menu == "Grounding & Breathing":
    st.title("🌿 Grounding & De-Stress")
    st.write("Choose a gentle exercise to help bring your attention back to the present moment.")

    st.subheader("5-4-3-2-1 Sensory Grounding")
    st.caption("Move through the senses at your own pace. You can skip a step or stop whenever you like.")

    grounding_steps = [
        ("5 things you can see", "Look around slowly and name five things you can see. Notice their colors, shapes, or details."),
        ("4 things you can feel", "Notice four physical sensations, such as your feet on the floor or the chair supporting you."),
        ("3 things you can hear", "Pause and notice three sounds nearby or in the distance."),
        ("2 things you can smell", "Notice two familiar scents, or recall two scents you find comforting. Don’t seek out strong smells."),
        ("1 thing you can taste", "Notice a taste that is already there, or sip water if you want. There is no need to try anything unfamiliar."),
    ]

    if "grounding_step" not in st.session_state:
        st.session_state["grounding_step"] = 0

    step_index = st.session_state["grounding_step"]
    if step_index >= len(grounding_steps):
        st.success("You’ve completed the grounding exercise. Take a moment to notice how you feel.")
        if st.button("Start again", key="grounding_restart"):
            st.session_state["grounding_step"] = 0
            st.rerun()
    else:
        step_title, step_prompt = grounding_steps[step_index]
        st.progress((step_index + 1) / len(grounding_steps))
        st.markdown(f"### Step {step_index + 1} of {len(grounding_steps)}: {step_title}")
        st.write(step_prompt)
        st.text_area(
            "Your notes (optional)",
            key=f"grounding_notes_{step_index}",
            height=100,
            placeholder="You can type a few words or simply notice them quietly.",
        )

        previous_col, next_col = st.columns(2)
        with previous_col:
            if step_index > 0 and st.button("Previous", key="grounding_previous"):
                st.session_state["grounding_step"] -= 1
                st.rerun()
        with next_col:
            next_label = "Finish exercise" if step_index == len(grounding_steps) - 1 else "Next sense"
            if st.button(next_label, key="grounding_next"):
                st.session_state["grounding_step"] += 1
                st.rerun()

    st.markdown("---")
    st.subheader("Box Breathing")
    st.write("Follow a gentle 4-4-4-4 rhythm. If holding your breath feels uncomfortable, breathe normally instead.")

    if st.button("Start 1-Cycle Calming Exercise"):
        box_placeholder = st.empty()
        stages = [
            ("Inhale slowly through your nose...", 4),
            ("Hold breath gently...", 4),
            ("Exhale steadily through your mouth...", 4),
            ("Rest and pause...", 4)
        ]
        for stage, duration in stages:
            for remaining in range(duration, 0, -1):
                box_placeholder.info(f"### {stage}\n\n⏱️ **{remaining} seconds**")
                time.sleep(1)
            box_placeholder.success("Cycle complete. Take a moment to relax your posture.")

    st.markdown("---")
    st.subheader("Progressive Muscle Relaxation")
    st.write("Move through one muscle group at a time. Gently tense for about 5 seconds, then release for about 10 seconds and notice the difference.")
    st.caption("Keep breathing normally. Use only gentle effort, skip any area that feels uncomfortable, and avoid tensing an injured area.")

    pmr_steps = [
        ("Hands and arms", "Curl your hands gently and tighten your forearms. Release your hands and let your arms rest."),
        ("Shoulders", "Raise your shoulders gently toward your ears. Release them and let them settle."),
        ("Face and jaw", "Softly scrunch your face or bring your teeth near each other without clenching. Release your jaw and smooth your face."),
        ("Stomach", "Gently tighten your stomach muscles without holding your breath. Release and let your belly soften."),
        ("Legs and feet", "Point or curl your toes gently and tighten your legs a little. Release and let your feet and legs rest."),
    ]

    if "pmr_active" not in st.session_state:
        st.session_state["pmr_active"] = False
    if "pmr_step" not in st.session_state:
        st.session_state["pmr_step"] = 0

    if not st.session_state["pmr_active"]:
        if st.button("Start guided PMR", key="pmr_start"):
            st.session_state["pmr_active"] = True
            st.session_state["pmr_step"] = 0
            st.rerun()
    elif st.session_state["pmr_step"] >= len(pmr_steps):
        st.success("You’ve completed the relaxation guide. Take a moment before returning to your day.")
        if st.button("Restart PMR", key="pmr_restart"):
            st.session_state["pmr_step"] = 0
            st.rerun()
        if st.button("Close PMR", key="pmr_close_complete"):
            st.session_state["pmr_active"] = False
            st.session_state["pmr_step"] = 0
            st.rerun()
    else:
        pmr_index = st.session_state["pmr_step"]
        pmr_title, pmr_prompt = pmr_steps[pmr_index]
        st.progress((pmr_index + 1) / len(pmr_steps))
        st.markdown(f"### Step {pmr_index + 1} of {len(pmr_steps)}: {pmr_title}")
        st.write(pmr_prompt)
        previous_col, next_col, finish_col = st.columns(3)
        with previous_col:
            if pmr_index > 0 and st.button("Previous area", key="pmr_previous"):
                st.session_state["pmr_step"] -= 1
                st.rerun()
        with next_col:
            next_label = "Finish guide" if pmr_index == len(pmr_steps) - 1 else "Next area"
            if st.button(next_label, key="pmr_next"):
                st.session_state["pmr_step"] += 1
                st.rerun()
        with finish_col:
            if st.button("Stop", key="pmr_stop"):
                st.session_state["pmr_active"] = False
                st.session_state["pmr_step"] = 0
                st.rerun()

    st.markdown("---")
    st.subheader("Ambient Soundscapes & White Noise")
    st.write("Choose a sound and duration, then generate a clip. Use the player to play, pause, or replay it.")

    soundscape = st.selectbox(
        "Choose a sound",
        [
            "White noise",
            "Pink noise",
            "Brown noise",
            "Gentle rainfall",
            "Ocean waves",
            "Running stream",
            "Forest birds",
            "Soft guitar melody",
        ],
        key="ambient_soundscape",
    )
    duration_seconds = st.slider(
        "Audio length (seconds)",
        min_value=3,
        max_value=60,
        value=15,
        key="ambient_duration",
    )
    if st.button("Generate selected sound", key="generate_ambient_audio"):
        st.session_state["ambient_audio"] = create_ambient_audio(soundscape, duration_seconds)
        st.session_state["ambient_audio_label"] = f"{soundscape} · {duration_seconds} seconds"

    if st.session_state.get("ambient_audio"):
        st.audio(st.session_state["ambient_audio"], format="audio/wav")
        st.caption(f"Generated locally: {st.session_state['ambient_audio_label']}")

# --- 7. DAILY AFFIRMATION ---
elif menu == "Daily Affirmation":
    st.title("✨ Daily Perspective")
    st.write("A gentle reminder for today.")

    if st.button("Show a new affirmation"):
        affirmations = [
            "I can take today one step at a time.",
            "Rest is a useful part of caring for myself.",
            "I deserve patience, including from myself.",
            "Small steps still count as progress.",
            "I can ask someone I trust for support.",
        ]
        st.markdown(f"### {random.choice(affirmations)}")

# --- 8. SLEEP HYGIENE & DIGITAL WIND-DOWN ---
elif menu == "Sleep Wind-Down":
    st.title("🌙 Sleep Hygiene & Digital Wind-Down")
    st.write("A gentle transition from late-night study to rest, designed for long laptop sessions.")

    st.html(
        """
        <section class="winddown-timer" aria-label="30-minute digital wind-down timer">
            <div class="winddown-label">30-minute digital detox</div>
            <div id="winddown-clock" class="winddown-clock" role="timer" aria-live="polite">30:00</div>
            <p id="winddown-status" class="winddown-status">Start when you’re ready, then step away from your devices.</p>
            <div class="winddown-actions">
                <button id="winddown-start" type="button">Start wind-down</button>
                <button id="winddown-pause" type="button" disabled>Pause</button>
                <button id="winddown-reset" type="button">Reset</button>
            </div>
        </section>
        <script>
        (() => {
            const storageKey = "mindcare-winddown-timer";
            const clock = document.getElementById("winddown-clock");
            const status = document.getElementById("winddown-status");
            const startButton = document.getElementById("winddown-start");
            const pauseButton = document.getElementById("winddown-pause");
            const resetButton = document.getElementById("winddown-reset");
            if (!clock || !status || !startButton || !pauseButton || !resetButton) return;

            if (window.mindcareWinddownInterval) clearInterval(window.mindcareWinddownInterval);
            let saved = {};
            try { saved = JSON.parse(sessionStorage.getItem(storageKey) || "{}"); } catch (_) {}
            let remaining = Number.isFinite(saved.remaining) ? saved.remaining : 1800;
            let deadline = Number.isFinite(saved.deadline) ? saved.deadline : null;

            const save = () => sessionStorage.setItem(storageKey, JSON.stringify({ remaining, deadline }));
            const draw = () => {
                if (deadline !== null) remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
                const minutes = Math.floor(remaining / 60).toString().padStart(2, "0");
                const seconds = (remaining % 60).toString().padStart(2, "0");
                clock.textContent = `${minutes}:${seconds}`;
                if (remaining === 0) {
                    deadline = null;
                    clearInterval(window.mindcareWinddownInterval);
                    window.mindcareWinddownInterval = null;
                    startButton.disabled = false;
                    pauseButton.disabled = true;
                    startButton.textContent = "Start again";
                    status.textContent = "Your wind-down is complete. Let your evening settle and get some rest.";
                    save();
                }
            };
            const run = () => {
                if (remaining <= 0) remaining = 1800;
                deadline = Date.now() + remaining * 1000;
                startButton.textContent = "Timer running";
                startButton.disabled = true;
                pauseButton.disabled = false;
                status.textContent = "Your timer is running. You can step away while it counts down.";
                window.mindcareWinddownInterval = setInterval(() => { draw(); save(); }, 1000);
                save();
                draw();
            };

            startButton.disabled = deadline !== null;
            pauseButton.disabled = deadline === null;
            if (deadline !== null) {
                startButton.textContent = "Timer running";
                status.textContent = "Your timer is running. You can step away while it counts down.";
                window.mindcareWinddownInterval = setInterval(() => { draw(); save(); }, 1000);
            } else if (remaining < 1800 && remaining > 0) {
                startButton.textContent = "Resume wind-down";
                status.textContent = "Your timer is paused. Resume whenever you’re ready.";
            }
            draw();

            startButton.addEventListener("click", run);
            pauseButton.addEventListener("click", () => {
                draw();
                deadline = null;
                clearInterval(window.mindcareWinddownInterval);
                window.mindcareWinddownInterval = null;
                startButton.disabled = false;
                startButton.textContent = "Resume wind-down";
                pauseButton.disabled = true;
                status.textContent = "Your timer is paused. Resume whenever you’re ready.";
                save();
            });
            resetButton.addEventListener("click", () => {
                remaining = 1800;
                deadline = null;
                clearInterval(window.mindcareWinddownInterval);
                window.mindcareWinddownInterval = null;
                startButton.disabled = false;
                startButton.textContent = "Start wind-down";
                pauseButton.disabled = true;
                status.textContent = "Start when you’re ready, then step away from your devices.";
                save();
                draw();
            });
        })();
        </script>
        """,
        unsafe_allow_javascript=True,
    )

    st.subheader("Sleep hygiene checklist")
    st.caption("No need to get everything perfect. Start with what feels doable tonight.")
    checklist = [
        st.checkbox("Blue light filter enabled on screen.", key="sleep_blue_light"),
        st.checkbox("Phone placed at least 3 feet away from pillow.", key="sleep_phone_distance"),
        st.checkbox("Drank one cup of room-temperature water.", key="sleep_water"),
        st.checkbox("Unclenched jaw and dropped shoulders.", key="sleep_relax_shoulders"),
    ]
    completed_items = sum(checklist)
    st.progress(completed_items / len(checklist), text=f"{completed_items} of {len(checklist)} complete")