#!/bin/bash
# Ganidhuz-FoxX: Export X/Twitter cookies from real Firefox snap profile
# Run this when session expires. Close Firefox first!
# 
# Config via env vars:
#   FIREFOX_PROFILE_PATH  - path to Firefox profile dir (default: auto-detect)
#   FOXX_COOKIES_OUT      - output path for cookies JSON (default: ./secrets/x-cookies.json)

set -e

# Auto-detect Firefox profile
if [ -n "$FIREFOX_PROFILE_PATH" ]; then
    PROFILE_PATH="$FIREFOX_PROFILE_PATH"
elif [ -f "$HOME/snap/firefox/common/.mozilla/firefox/profiles.ini" ]; then
    PROFILE_DIR="$HOME/snap/firefox/common/.mozilla/firefox"
    PROFILE_NAME=$(grep "^Path=" "$PROFILE_DIR/profiles.ini" | head -1 | cut -d= -f2)
    PROFILE_PATH="$PROFILE_DIR/$PROFILE_NAME"
elif [ -f "$HOME/.mozilla/firefox/profiles.ini" ]; then
    PROFILE_DIR="$HOME/.mozilla/firefox"
    PROFILE_NAME=$(grep "^Path=" "$PROFILE_DIR/profiles.ini" | head -1 | cut -d= -f2)
    PROFILE_PATH="$PROFILE_DIR/$PROFILE_NAME"
else
    echo "❌ Could not find Firefox profile. Set FIREFOX_PROFILE_PATH env var."
    exit 1
fi

DB="$PROFILE_PATH/cookies.sqlite"
TMP_DB="/tmp/foxx-cookies-copy.sqlite"
OUT="${FOXX_COOKIES_OUT:-$(dirname "$0")/../secrets/x-cookies.json}"

mkdir -p "$(dirname "$OUT")"

echo "🦊 Ganidhuz-FoxX: Exporting X cookies from $PROFILE_PATH"

pkill -f firefox 2>/dev/null && sleep 2 || true

cp "$DB" "$TMP_DB"

python3 - << EOF
import sqlite3, json

conn = sqlite3.connect("$TMP_DB")
rows = conn.execute("""
    SELECT host, name, value, path, expiry, isSecure, isHttpOnly, sameSite
    FROM moz_cookies
    WHERE host LIKE '%twitter%' OR host LIKE '%x.com%'
""").fetchall()

cookies = []
for r in rows:
    exp = r[4]
    if exp > 1e10:
        exp = int(exp / 1000)
    elif exp < -1:
        exp = -1
    cookies.append({
        "domain": r[0], "name": r[1], "value": r[2],
        "path": r[3], "expires": exp, "secure": bool(r[5]),
        "httpOnly": bool(r[6]),
        "sameSite": ["None","Lax","Strict"][r[7]] if r[7] < 3 else "None"
    })
conn.close()

with open("$OUT", "w") as f:
    json.dump({"cookies": cookies}, f, indent=2)

print(f"✅ Exported {len(cookies)} cookies -> $OUT")
EOF
