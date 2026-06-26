import os
from pathlib import Path


def write_restricted(path: Path, content: str):
    """Write a file that is only readable by the owner (0o600)."""
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        f.write(content)

# Base directory for tokens and credentials — restricted permissions
DATA_DIR = Path.home() / ".calintegration"
DATA_DIR.mkdir(mode=0o700, exist_ok=True)

# Load .env file if present
_env_file = DATA_DIR / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            os.environ.setdefault(key.strip(), value)

# Source calendar — any ICS/iCal feed URL (secret: may grant read access to calendar)
ICS_URL = os.environ.get("CALINT_ICS_URL", "") or os.environ.get("CALINT_GOOGLE_ICS_URL", "")

# Microsoft Graph settings (PublicClient — no client secret needed)
MS_TOKEN_FILE = DATA_DIR / "ms_token.json"
MS_CLIENT_ID = os.environ.get("CALINT_MS_CLIENT_ID", "")
MS_TENANT_ID = os.environ.get("CALINT_MS_TENANT_ID", "")
MS_AUTHORITY = f"https://login.microsoftonline.com/{MS_TENANT_ID}"
MS_SCOPES = ["Calendars.ReadWrite"]

# Sync settings
SYNC_DAYS_AHEAD = 14
EVENT_MAP_FILE = DATA_DIR / "event_map.json"
LOG_FILE = DATA_DIR / "sync.log"
BLOCKED_EVENT_TITLE = "Blocked"

# Exchange Calendar ID to sync to (default: primary)
MS_CALENDAR_ID = os.environ.get("CALINT_MS_CALENDAR_ID", None)
