"""
config.py — Centralized configuration loaded from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenAI (image generation) ──────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
IMAGE_MODEL: str = os.getenv("IMAGE_MODEL", "dall-e-3")

# ── Google Gemini (content generation) ─────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ── Apify (Facebook scraping) ─────────────────────────────
APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")
APIFY_TIMEOUT_SECS: int = int(os.getenv("APIFY_TIMEOUT_SECS", "300"))
APIFY_MAX_PAGES: int = int(os.getenv("APIFY_MAX_PAGES", "1"))

# ── Facebook App ───────────────────────────────────────────
FB_APP_ID: str = os.getenv("FB_APP_ID", "")
FB_APP_SECRET: str = os.getenv("FB_APP_SECRET", "")
FB_CLIENT_TOKEN: str = os.getenv("FB_CLIENT_TOKEN", "")

# ── Facebook Page ──────────────────────────────────────────
FB_PAGE_ID: str = os.getenv("FB_PAGE_ID", "")
FB_USER_ACCESS_TOKEN: str = os.getenv("FB_USER_ACCESS_TOKEN", "")
FB_PAGE_ACCESS_TOKEN: str = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
FB_API_VERSION: str = os.getenv("API_VERSION", "v21.0")
FB_BASE_URL: str = f"https://graph.facebook.com/{FB_API_VERSION}"

# ── Content generation ─────────────────────────────────────
CONTENT_LANGUAGE: str = os.getenv("CONTENT_LANGUAGE", "vi")
MAX_CAPTION_LENGTH: int = int(os.getenv("MAX_CAPTION_LENGTH", "500"))

# ── Runtime ────────────────────────────────────────────────
MAX_POST_RETRIES: int = int(os.getenv("MAX_POST_RETRIES", "3"))
POST_DELAY_SECONDS: int = int(os.getenv("POST_DELAY_SECONDS", "2"))



def validate(mode: str = "publish"):
    """Kiểm tra các biến môi trường bắt buộc.

    Args:
        mode: 'publish' requires FB + Gemini + Apify keys;
              'analyze' requires only Gemini + Apify keys.
    """
    missing = []

    # Always required
    required = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "APIFY_API_TOKEN": APIFY_API_TOKEN,
    }

    if mode == "publish":
        required.update({
            "FB_APP_ID": FB_APP_ID,
            "FB_APP_SECRET": FB_APP_SECRET,
            "FB_PAGE_ID": FB_PAGE_ID,
        })

    for name, val in required.items():
        if not val:
            missing.append(name)
    if missing:
        raise EnvironmentError(
            f"❌ Thiếu biến môi trường: {', '.join(missing)}\n"
            "→ Kiểm tra file .env"
        )
