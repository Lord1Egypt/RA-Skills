#!/bin/sh
# Thin bootstrap — install ardi-agent if missing, then run preflight.
# Called by skill-runner frameworks (OpenClaw / Hermes / agentskills.io)
# as the first action after the skill is fetched.
set -e
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
export PATH="$INSTALL_DIR:$PATH"

if ! command -v ardi-agent >/dev/null 2>&1; then
  TMP="$(mktemp)"
  URL="https://raw.githubusercontent.com/awp-worknet/ardi-skill/main/install.sh"
  if   command -v curl    >/dev/null 2>&1; then curl -fsSL -o "$TMP" "$URL"
  elif command -v wget    >/dev/null 2>&1; then wget -qO  "$TMP" "$URL"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "import sys, urllib.request; urllib.request.urlretrieve(sys.argv[1], sys.argv[2])" "$URL" "$TMP"
  else
    echo "need curl, wget, or python3 to fetch ardi-agent" >&2; exit 1
  fi
  INSTALL_DIR="$INSTALL_DIR" sh "$TMP"
fi

exec ardi-agent preflight
