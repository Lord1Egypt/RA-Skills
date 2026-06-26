#!/usr/bin/env bash
# smart-search/scripts/setup.sh
# One-time setup: creates required directories, quota file scaffold, and
# verifies Node.js and proper-lockfile are available.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
SHARED_DIR="$OPENCLAW_DIR/workspace/shared"
QUOTA_PATH="${SEARCH_QUOTA_PATH:-$SHARED_DIR/search-quota.json}"
LOGS_DIR="$(dirname "$QUOTA_PATH")/logs"

echo "[setup] smart-search setup starting..."

# ── 1. Node.js check ──────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  echo "[setup] ERROR: node is not installed. Install Node.js 18+ and re-run."
  exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "[setup] WARNING: Node.js $NODE_VERSION detected. Node 18+ is recommended."
fi

echo "[setup] Node.js $NODE_VERSION found."

# ── 2. Install dependencies ───────────────────────────────────────────────────
echo "[setup] Installing npm dependencies..."
cd "$SKILL_DIR"
npm install --silent
echo "[setup] Dependencies installed."

# ── 3. Create directories ─────────────────────────────────────────────────────
mkdir -p "$SHARED_DIR" "$LOGS_DIR"
echo "[setup] Directories created: $SHARED_DIR"

# ── 4. Scaffold quota file if missing ────────────────────────────────────────
if [ ! -f "$QUOTA_PATH" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$QUOTA_PATH" << JSON
{
  "date": "$TODAY",
  "providers": {
    "gemini": { "daily_limit": 0, "remaining": 0, "used": 0, "shared_pool": 0 },
    "brave":  { "daily_limit": 0, "remaining": 0, "used": 0, "shared_pool": 0 }
  },
  "agent_allocations": {}
}
JSON
  echo "[setup] Created quota file: $QUOTA_PATH"
else
  echo "[setup] Quota file already exists: $QUOTA_PATH"
fi

# ── 5. Check openclaw.json ────────────────────────────────────────────────────
CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$OPENCLAW_DIR/openclaw.json}"
if [ ! -f "$CONFIG_PATH" ]; then
  echo ""
  echo "[setup] WARNING: openclaw.json not found at $CONFIG_PATH"
  echo "        Create it and add your API keys and skill config."
  echo "        See references/openclaw-config.md for a full example."
else
  # Check for smart-search block
  if ! grep -q '"smart-search"' "$CONFIG_PATH" 2>/dev/null; then
    echo ""
    echo "[setup] WARNING: No smart-search config found in openclaw.json."
    echo "        Add the skills.smart-search block — see references/openclaw-config.md."
  else
    echo "[setup] openclaw.json contains smart-search config. ✓"
  fi

  # Check for API keys
  if ! grep -q 'GEMINI_API_KEY' "$CONFIG_PATH" 2>/dev/null; then
    echo "[setup] WARNING: GEMINI_API_KEY not found in openclaw.json env block."
  fi
  if ! grep -q 'BRAVE_API_KEY' "$CONFIG_PATH" 2>/dev/null; then
    echo "[setup] WARNING: BRAVE_API_KEY not found in openclaw.json env block."
  fi
fi

echo ""
echo "[setup] ✓ smart-search setup complete."
echo "        Run a test: echo '{\"tool\":\"search_quota_status\",\"args\":{}}' | node $SKILL_DIR/index.js"
