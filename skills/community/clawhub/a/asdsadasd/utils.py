"""
utils.py — Shared utility helpers: logging, URL validation, text cleaning.
"""
import re
import logging
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("openclaw")


def validate_url(url: str) -> tuple[bool, str]:
    """Validate if a string is a proper URL.

    Returns:
        (is_valid, cleaned_url_or_error_message)
    """
    url = url.strip()
    if not url:
        return False, "URL is empty"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, f"Invalid URL: no domain found in '{url}'"
        return True, url
    except Exception as e:
        return False, f"Invalid URL: {e}"


def detect_source_type(url: str) -> str:
    """Detect the type of source from a URL."""
    domain = urlparse(url).netloc.lower()

    if "facebook.com" in domain or "fb.com" in domain:
        return "facebook"
    elif "dantri.com" in domain:
        return "dantri"
    elif "vnexpress.net" in domain:
        return "vnexpress"
    elif "thanhnien.vn" in domain:
        return "thanhnien"
    elif "tuoitre.vn" in domain:
        return "tuoitre"
    else:
        return "website"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length, ending at a word boundary."""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + "..."


def clean_text(text: str) -> str:
    """Clean scraped text: remove extra whitespace, normalize newlines."""
    if not text:
        return ""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def alert_inaccessible(url: str, reason: str) -> None:
    """Alert when a URL is inaccessible."""
    logger.warning(
        f"🚨 ALERT: Cannot access URL\n"
        f"   URL: {url}\n"
        f"   Reason: {reason}\n"
        f"   Action: Please check the URL manually or try again later."
    )
