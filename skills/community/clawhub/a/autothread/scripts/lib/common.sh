# common.sh — shared helpers for all autothread platform adapters.
#
# DISCLOSURE: the helpers in this file read the local OpenClaw config
# file (~/.openclaw/openclaw.json, or $OPENCLAW_CONFIG), which contains
# credential-bearing values such as bot tokens and the Signal account.
# Values read from it are used solely to authenticate calls to the
# platform API of the invoked adapter (api.telegram.org, discord.com)
# or to address the local signal-cli daemon. No data is transmitted to
# any other destination. See SKILL.md "Privacy & data handling".
#
# Sourced by autothread-*.sh. Expects caller to have `set -o pipefail`.

# ── dependency check ────────────────────────────────────────────────
autothread_require() {
  for cmd in "$@"; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "ERROR: '$cmd' is required but not found in PATH" >&2
      exit 1
    fi
  done
}

# ── OpenClaw config ─────────────────────────────────────────────────
AUTOTHREAD_CONFIG_FILE="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

autothread_config_path() {
  if [ ! -f "$AUTOTHREAD_CONFIG_FILE" ]; then
    echo "ERROR: OpenClaw config not found at $AUTOTHREAD_CONFIG_FILE" >&2
    exit 1
  fi
  printf '%s' "$AUTOTHREAD_CONFIG_FILE"
}

# Read a jq path from the OpenClaw config; exits 1 if empty.
autothread_config_get() {
  # $1 = jq filter (e.g. '.channels.telegram.botToken // empty')
  local value
  value=$(jq -r "$1" "$AUTOTHREAD_CONFIG_FILE" 2>/dev/null)
  if [ -z "$value" ] || [ "$value" = "null" ]; then
    echo "ERROR: config path '$1' not found or empty in $AUTOTHREAD_CONFIG_FILE" >&2
    exit 1
  fi
  printf '%s' "$value"
}

# ── text helpers ────────────────────────────────────────────────────
# Trim leading/trailing whitespace
autothread_trim() {
  printf '%s' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

# HTML-escape a string (for Telegram parse_mode=HTML)
autothread_html_escape() {
  printf '%s' "$1" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g'
}

# ── title fallback ──────────────────────────────────────────────────
# Generate a concise title from message text: first line, cut to ~50
# chars at a word boundary, with an ellipsis when truncated.
# $1 = message text, $2 = optional max length override
autothread_fallback_title() {
  local msg first_line title len max
  msg=$(autothread_trim "$1")
  max="${2:-50}"
  if [ -z "$msg" ]; then
    printf 'New Topic'
    return
  fi
  first_line=$(printf '%s' "$msg" | head -1)
  len=${#first_line}
  title=$(printf '%s' "$first_line" | cut -c1-"$max" | sed 's/[[:space:]][^[:space:]]*$//')
  title=$(autothread_trim "$title")
  if [ "$len" -gt "$max" ]; then
    title="${title}…"
  fi
  printf '%s' "$title"
}

# ── JSON output (the adapter contract) ──────────────────────────────
# Every adapter prints exactly this on stdout on success:
#   {"topic_id": <id|string>, "title": "<title>", "link": <url|null>}
# An empty link (Signal has no shareable URLs) is emitted as JSON null.
autothread_emit_result() {
  # $1 = topic id (number or string), $2 = title, $3 = link (may be empty)
  local link_json
  if [ -n "$3" ]; then
    link_json=$(jq -Rn --arg link "$3" '$link')
  else
    link_json="null"
  fi
  if printf '%s' "$1" | grep -qE '^-?[0-9]+$'; then
    jq -n --argjson tid "$1" --arg title "$2" --argjson link "$link_json" \
      '{"topic_id": $tid, "title": $title, "link": $link}'
  else
    jq -n --arg tid "$1" --arg title "$2" --argjson link "$link_json" \
      '{"topic_id": $tid, "title": $title, "link": $link}'
  fi
}

# ── JSON string escaping (for REST payloads) ────────────────────────
autothread_json_escape() {
  jq -Rn --arg s "$1" '$s'
}
