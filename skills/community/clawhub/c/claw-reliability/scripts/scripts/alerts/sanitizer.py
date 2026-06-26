"""
claw-reliability: Alert sanitizer.
Redacts sensitive values from alert text and details before sending to
external destinations.
"""

import re
import os

_REDACTED = "[REDACTED]"

_PATTERNS = [
    # Anthropic API keys
    re.compile(r'sk-ant-[A-Za-z0-9\-_]{10,}'),
    # OpenAI / generic sk- keys
    re.compile(r'sk-[A-Za-z0-9\-_]{10,}'),
    # Slack tokens
    re.compile(r'xox[bparos]-[A-Za-z0-9\-]+'),
    # Discord and Slack webhook URLs
    re.compile(r'https://discord\.com/api/webhooks/[^\s"\']+'),
    re.compile(r'https://hooks\.slack\.com/[^\s"\']+'),
    # Generic webhook URLs (any path under common webhook hosts)
    re.compile(r'https?://[^\s"\']+/webhooks?/[^\s"\']+'),
]

# Home directory prefix — built at import time, e.g. /home/fiddy or /Users/fiddy
_HOME = os.path.expanduser("~")


def sanitize_text(text: str) -> str:
    """Redact sensitive patterns from a string."""
    if not isinstance(text, str):
        return text
    for pattern in _PATTERNS:
        text = pattern.sub(_REDACTED, text)
    if _HOME and _HOME != "~":
        text = text.replace(_HOME, "~")
    return text


def sanitize_details(details: dict) -> dict:
    """Return a copy of details with all string values sanitized."""
    if not details:
        return details
    return {k: sanitize_text(v) if isinstance(v, str) else v
            for k, v in details.items()}
