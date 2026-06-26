#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <GA4_PROPERTY_ID> <PATH_TO_CLIENT_SECRET_JSON>"
  exit 1
fi

PROPERTY_ID="$1"
CLIENT_JSON="$2"
CONFIG_DIR="$HOME/.config/openclaw"
mkdir -p "$CONFIG_DIR"

if [[ ! -f "$CLIENT_JSON" ]]; then
  echo "Client secret JSON not found: $CLIENT_JSON"
  exit 1
fi

python3 -m pip install --user google-analytics-data google-auth-oauthlib google-auth-httplib2
cp "$CLIENT_JSON" "$CONFIG_DIR/ga4-client.json"

SHELL_RC="$HOME/.zshrc"
if [[ -n "${BASH_VERSION:-}" ]]; then
  SHELL_RC="$HOME/.bashrc"
fi

python3 - <<PY
from pathlib import Path
import re
rc = Path("$SHELL_RC")
text = rc.read_text() if rc.exists() else ""
text = re.sub(r'^export GA4_PROPERTY_ID=.*\\n?', '', text, flags=re.M)
if text and not text.endswith('\\n'):
    text += '\\n'
text += 'export GA4_PROPERTY_ID="$PROPERTY_ID"\\n'
rc.write_text(text)
print(f"Updated {rc}")
PY

echo
echo "Installed GA4 deps and config."
echo "Next step: authorize once via"
echo "  python3 ~/.openclaw/workspace/scripts/ga4_query.py --metrics activeUsers,sessions --dimensions date --start 7daysAgo --end today --pretty"
echo
