"""
SKILL.md safety detectors.

Each detector scans skill content for dangerous patterns based on
the ClawHavoc incident analysis and OWASP agent security guidelines.
"""

import re

# ── Credential harvesting: accessing known secret env var names ─────────────

_CREDENTIAL_RE = re.compile(
    r"(?i)"
    r"\$\{?\s*(?:"
    r"[A-Z_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|PRIVATE_KEY|CREDENTIALS?|AUTH)"
    r"[A-Z_]*"
    r")\s*\}?",
)

# ── Data exfiltration: sending data to external URLs ────────────────────────

_EXFIL_RE = re.compile(
    r"(?i)"
    r"(?:curl|wget|httpx|requests?\s*\.\s*(?:get|post|put)|"
    r"fetch\s*\(|nc\s+-)"
    r"[^\n]*"
    r"https?://",
)

# ── Obfuscated commands: base64 decode piped to shell, eval, exec ───────────

_OBFUSCATED_RE = re.compile(
    r"(?i)"
    r"(?:base64\s+(?:-d|--decode)|"
    r"\beval\b\s*[\($]|"
    r"\bexec\b\s*[\($]|"
    r"\bsource\s+/dev/|"
    r"python\s+-c\s+['\"].*(?:exec|eval)|"
    r"echo\s+['\"][A-Za-z0-9+/=]+['\"]\s*\|\s*(?:base64|bash|sh))",
)

# ── Permission overreach: sensitive filesystem, shell spawning ──────────────

_OVERREACH_RE = re.compile(
    r"(?i)"
    r"(?:/etc/(?:shadow|passwd|sudoers)|"
    r"/root/|~root/|"
    r"\.ssh/|\.gnupg/|"
    r"reverse\s*shell|"
    r"bash\s+-i\s*>&|"
    r"/dev/tcp/|"
    r"mkfifo\s+|"
    r"chmod\s+[0-7]*777|"
    r"rm\s+-rf\s+/)",
)

# ── Detector registry ───────────────────────────────────────────────────────

DETECTORS: list[tuple[str, re.Pattern[str]]] = [
    ("credential_harvesting", _CREDENTIAL_RE),
    ("data_exfiltration", _EXFIL_RE),
    ("obfuscated_command", _OBFUSCATED_RE),
    ("permission_overreach", _OVERREACH_RE),
]

TOTAL_PATTERNS = len(DETECTORS)


def scan(content: str) -> list[str]:
    """Scan SKILL.md content and return list of detected threat names."""
    return [name for name, pattern in DETECTORS if pattern.search(content)]
