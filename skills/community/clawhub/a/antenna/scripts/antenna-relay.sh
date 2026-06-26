#!/usr/bin/env bash
# antenna-relay.sh — Deterministic relay processor for inbound Antenna messages.
# Parses [ANTENNA_RELAY] envelope, validates, formats delivery message, logs.
# Called by the Antenna agent via exec. Outputs JSON to stdout.
#
# Usage:
#   antenna-relay.sh <raw_message>
#   echo "<raw_message>" | antenna-relay.sh --stdin
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"

# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"
# shellcheck source=../lib/config.sh
source "$SKILL_DIR/lib/config.sh"

# ── Helpers ──────────────────────────────────────────────────────────────────

json_ok() {
  jq -n \
    --arg sessionKey "$1" \
    --arg message "$2" \
    --arg from "$3" \
    --arg timestamp "$4" \
    --argjson chars "$5" \
    '{action:"relay", status:"ok", sessionKey:$sessionKey, message:$message, from:$from, timestamp:$timestamp, chars:$chars}'
}

json_reject() {
  local reason="$1"
  local from="${2:-unknown}"
  jq -n \
    --arg reason "$reason" \
    --arg from "$from" \
    '{action:"reject", status:"rejected", reason:$reason, from:$from}'
}

json_malformed() {
  local reason="$1"
  jq -n \
    --arg reason "$reason" \
    '{action:"reject", status:"malformed", reason:$reason}'
}

sanitize_log_value() {
  # Strip newlines, carriage returns, and control characters; truncate to max length
  local value="$1"
  local max_len="${2:-200}"
  # Replace control chars (including newlines/tabs) with spaces
  value=$(echo "$value" | tr '\n\r\t' '   ' | sed 's/[[:cntrl:]]//g')
  # Collapse multiple spaces and trim leading/trailing whitespace
  value=$(echo "$value" | sed 's/  */ /g; s/^ //; s/ $//')
  # Truncate
  if [[ ${#value} -gt $max_len ]]; then
    value="${value:0:$max_len}…"
  fi
  echo "$value"
}

secret_equal_constant_time() {
  local left="$1" right="$2"

  if command -v python3 >/dev/null 2>&1; then
    python3 - "$left" "$right" <<'PY'
import hmac
import sys
sys.exit(0 if hmac.compare_digest(sys.argv[1], sys.argv[2]) else 1)
PY
    return $?
  fi

  local left_hash right_hash
  left_hash=$(printf '%s' "$left" | sha256sum | awk '{print $1}')
  right_hash=$(printf '%s' "$right" | sha256sum | awk '{print $1}')
  [[ "$left_hash" == "$right_hash" ]]
}

log_entry() {
  local log_enabled log_path
  log_enabled=$(config_log_enabled)
  log_path=$(config_log_path)

  if [[ "$log_enabled" != "true" ]]; then
    return 0
  fi

  # Resolve relative log path against skill dir
  if [[ "$log_path" != /* ]]; then
    log_path="$SKILL_DIR/$log_path"
  fi

  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$ts] $*" >> "$log_path"
}

# ── Read input ───────────────────────────────────────────────────────────────

if [[ "${1:-}" == "--stdin" ]]; then
  RAW_MESSAGE=$(cat)
elif [[ $# -ge 1 ]]; then
  RAW_MESSAGE="$1"
else
  json_malformed "No input provided"
  exit 0
fi

# ── Detect envelope markers ─────────────────────────────────────────────────

if ! echo "$RAW_MESSAGE" | grep -q '\[ANTENNA_RELAY\]'; then
  json_malformed "No [ANTENNA_RELAY] envelope detected"
  log_entry "INBOUND  | status:MALFORMED (no envelope markers)"
  exit 0
fi

if ! echo "$RAW_MESSAGE" | grep -q '\[/ANTENNA_RELAY\]'; then
  json_malformed "No closing [/ANTENNA_RELAY] marker"
  log_entry "INBOUND  | status:MALFORMED (no closing marker)"
  exit 0
fi

# Reject multiple envelope markers (collision/injection attempt)
OPEN_COUNT=$(echo "$RAW_MESSAGE" | grep -o '\[ANTENNA_RELAY\]' | wc -l | tr -d ' ')
CLOSE_COUNT=$(echo "$RAW_MESSAGE" | grep -o '\[/ANTENNA_RELAY\]' | wc -l | tr -d ' ')
if [[ "$OPEN_COUNT" -ne 1 || "$CLOSE_COUNT" -ne 1 ]]; then
  json_malformed "Multiple envelope markers detected"
  log_entry "INBOUND  | status:MALFORMED (multiple envelope markers)"
  exit 0
fi

# ── Extract envelope content ────────────────────────────────────────────────

# Get everything between [ANTENNA_RELAY] and [/ANTENNA_RELAY]
ENVELOPE=$(echo "$RAW_MESSAGE" | sed -n '/\[ANTENNA_RELAY\]/,/\[\/ANTENNA_RELAY\]/p' | sed '1d;$d')

# ── Parse headers ────────────────────────────────────────────────────────────
# Headers are key: value lines before the first blank line.
# Body is everything after the first blank line.

HEADERS=""
BODY=""
IN_BODY=false

while IFS= read -r line; do
  if [[ "$IN_BODY" == "true" ]]; then
    if [[ -n "$BODY" ]]; then
      BODY="${BODY}
${line}"
    else
      BODY="$line"
    fi
  elif [[ -z "$line" ]]; then
    IN_BODY=true
  else
    if [[ -n "$HEADERS" ]]; then
      HEADERS="${HEADERS}
${line}"
    else
      HEADERS="$line"
    fi
  fi
done <<< "$ENVELOPE"

# Extract individual header values
get_header() {
  echo "$HEADERS" | grep -i "^${1}:" | head -1 | sed "s/^${1}:[[:space:]]*//" || true
}

FROM=$(get_header "from")
REPLY_TO=$(get_header "reply_to")
TARGET_SESSION=$(get_header "target_session")
TIMESTAMP=$(get_header "timestamp")
SUBJECT=$(get_header "subject")
USER_NAME=$(get_header "user")

# ── Sanitize peer-supplied header values for safe logging/processing ────────
# Strips control chars, newlines, and truncates to prevent log injection.
FROM=$(sanitize_log_value "$FROM" 64)
REPLY_TO=$(sanitize_log_value "$REPLY_TO" 256)
TARGET_SESSION=$(sanitize_log_value "$TARGET_SESSION" 128)
TIMESTAMP=$(sanitize_log_value "$TIMESTAMP" 32)
SUBJECT=$(sanitize_log_value "$SUBJECT" 200)
USER_NAME=$(sanitize_log_value "$USER_NAME" 64)

# ── REF-400: reject reserved envelope markers inside parsed values ──────────
if [[ "$BODY" == *"[ANTENNA_RELAY]"* ]] || [[ "$BODY" == *"[/ANTENNA_RELAY]"* ]]; then
  json_malformed "Envelope markers detected inside body"
  log_entry "INBOUND  | status:MALFORMED (marker in body)"
  exit 0
fi

if [[ "$SUBJECT" == *"[ANTENNA_RELAY]"* ]] || [[ "$SUBJECT" == *"[/ANTENNA_RELAY]"* ]] || \
   [[ "$USER_NAME" == *"[ANTENNA_RELAY]"* ]] || [[ "$USER_NAME" == *"[/ANTENNA_RELAY]"* ]] || \
   [[ "$REPLY_TO" == *"[ANTENNA_RELAY]"* ]] || [[ "$REPLY_TO" == *"[/ANTENNA_RELAY]"* ]]; then
  json_malformed "Envelope markers detected inside header values"
  log_entry "INBOUND  | status:MALFORMED (marker in headers)"
  exit 0
fi

# ── REF-1502: extract optional correlation nonce from body ──────────────────
# The body may contain a `nonce: <value>` line (used by antenna-model-test.sh
# and anyone else who wants log correlation). Extract it with a strict
# character class to prevent log injection / ANSI / gigantic values. Default
# to `-` (absent) when nothing valid is present. This is NOT authentication;
# peers_get + peer secret verification already did that. The nonce is purely
# for scoping a receiver-side log scan to one caller's message.
NONCE=$(echo "$BODY" | grep -m1 -E '^nonce:[[:space:]]*[A-Za-z0-9_-]{1,40}[[:space:]]*$' \
  | sed -E 's/^nonce:[[:space:]]*([A-Za-z0-9_-]{1,40})[[:space:]]*$/\1/' || true)
NONCE="${NONCE:--}"

# ── Validate required fields ────────────────────────────────────────────────

if [[ -z "$FROM" ]]; then
  json_reject "Missing required field: from"
  log_entry "INBOUND  | nonce:$NONCE | status:REJECTED (missing from)"
  exit 0
fi

if [[ -z "$TARGET_SESSION" ]]; then
  # Use default from config; if absent, build full key for main session
  TARGET_SESSION=$(config_default_target_session)
  if [[ -z "$TARGET_SESSION" ]]; then
    LOCAL_AGENT=$(config_local_agent_id)
    TARGET_SESSION="agent:${LOCAL_AGENT}:main"
  fi
fi

if [[ -z "$TIMESTAMP" ]]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
fi

# ── REF-402: timestamp freshness window to limit replay exposure ───────────
TIMESTAMP_EPOCH=$(date -u -d "$TIMESTAMP" +%s 2>/dev/null || echo "")
if [[ -z "$TIMESTAMP_EPOCH" ]]; then
  json_malformed "Invalid timestamp format"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:MALFORMED (invalid timestamp)"
  exit 0
fi

NOW_EPOCH=$(date -u +%s)
MAX_AGE_SECONDS=$(config_get '.security.max_message_age_seconds' '300')
MAX_FUTURE_SKEW_SECONDS=$(config_get '.security.max_future_skew_seconds' '60')
AGE_SECONDS=$((NOW_EPOCH - TIMESTAMP_EPOCH))
FUTURE_SKEW_SECONDS=$((TIMESTAMP_EPOCH - NOW_EPOCH))

if (( AGE_SECONDS > MAX_AGE_SECONDS )); then
  json_reject "Message timestamp too old (${AGE_SECONDS}s > ${MAX_AGE_SECONDS}s)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (timestamp too old: ${AGE_SECONDS}s > ${MAX_AGE_SECONDS}s)"
  exit 0
fi

if (( FUTURE_SKEW_SECONDS > MAX_FUTURE_SKEW_SECONDS )); then
  json_reject "Message timestamp too far in future (${FUTURE_SKEW_SECONDS}s > ${MAX_FUTURE_SKEW_SECONDS}s)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (timestamp in future: ${FUTURE_SKEW_SECONDS}s > ${MAX_FUTURE_SKEW_SECONDS}s)"
  exit 0
fi

# ── Validate sender against allowed inbound peers ───────────────────────────

ALLOWED=$(jq -r --arg from "$FROM" '
  .allowed_inbound_peers // [] | if (. | length) == 0 then "allowed"
  elif (. | index($from)) then "allowed"
  else "denied" end
' "$CONFIG_FILE" 2>/dev/null || echo "allowed")

if [[ "$ALLOWED" == "denied" ]]; then
  json_reject "Unknown or disallowed sender: $FROM" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (not in allowed_inbound_peers)"
  exit 0
fi

# Also check peers file for existence
if ! peers_exists "$FROM"; then
  json_reject "Unknown peer: $FROM (not in peers registry)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (unknown peer)"
  exit 0
fi

# ── Per-peer authentication ──────────────────────────────────────────────────
# If the claimed sender has a peer_secret_file configured, we REQUIRE a matching
# auth: header. This binds identity to a shared secret — the from: field alone
# is no longer sufficient.

AUTH_HEADER=$(get_header "auth")
AUTH_HEADER=$(sanitize_log_value "$AUTH_HEADER" 128)

EXPECTED_SECRET_FILE=$(peers_get "$FROM" peer_secret_file)
if [[ -n "$EXPECTED_SECRET_FILE" ]]; then
  # Resolve relative paths against skill dir
  if [[ "$EXPECTED_SECRET_FILE" != /* ]]; then
    EXPECTED_SECRET_FILE="$SKILL_DIR/$EXPECTED_SECRET_FILE"
  fi

  if [[ ! -f "$EXPECTED_SECRET_FILE" ]]; then
    # Secret file configured but missing — fail closed
    json_reject "Peer auth configured but secret file missing for: $FROM" "$FROM"
    log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (peer secret file missing)"
    exit 0
  fi

  EXPECTED_SECRET=$(tr -d '[:space:]' < "$EXPECTED_SECRET_FILE")

  if [[ -z "$AUTH_HEADER" ]]; then
    json_reject "Peer auth required but no auth header provided (from: $FROM)" "$FROM"
    log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (missing auth header)"
    exit 0
  fi

  if ! secret_equal_constant_time "$AUTH_HEADER" "$EXPECTED_SECRET"; then
    # Diagnostic: provide actionable detail without exposing actual secrets
    auth_hint="${AUTH_HEADER:0:6}...${AUTH_HEADER: -4}"
    expected_hint="${EXPECTED_SECRET:0:6}...${EXPECTED_SECRET: -4}"
    diag_msg="Peer auth failed: invalid secret (from: $FROM). Received prefix/suffix: ${auth_hint}, expected prefix/suffix: ${expected_hint}. Likely cause: peer secrets are out of sync. Fix: re-run 'antenna peers exchange' between hosts to resync, or verify peer_secret_file points to the correct file on both sides."
    json_reject "Peer auth failed: invalid secret (from: $FROM)" "$FROM"
    log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (invalid peer secret) | hint:received=${auth_hint} expected=${expected_hint} | fix:resync peer secrets via 'antenna peers exchange'"
    exit 0
  fi

  log_entry "INBOUND  | from:$FROM | peer_auth:verified"
else
  # No per-peer secret configured — warn but allow (backward compat / migration)
  if [[ -n "$AUTH_HEADER" ]]; then
    log_entry "INBOUND  | from:$FROM | peer_auth:ignored (no secret configured, auth header present)"
  fi
fi

# ── Rate limiting ────────────────────────────────────────────────────────────

RATE_LIMIT_FILE="$SKILL_DIR/antenna-ratelimit.json"
RATE_LIMIT_LOCK_FILE="${RATE_LIMIT_FILE}.lock"
PEER_LIMIT=$(config_rate_limit_per_peer)
GLOBAL_LIMIT=$(config_rate_limit_global)

mkdir -p "$(dirname "$RATE_LIMIT_FILE")"
if [[ ! -f "$RATE_LIMIT_FILE" ]]; then
  echo '{}' > "$RATE_LIMIT_FILE"
fi

NOW_EPOCH=$(date +%s)
WINDOW_START=$((NOW_EPOCH - 60))

rate_limit_check_and_record() {
  local result tmp_file
  tmp_file="${RATE_LIMIT_FILE}.tmp.$$"

  result=$(jq -r --arg from "$FROM" --argjson now "$NOW_EPOCH" --argjson cutoff "$WINDOW_START" \
    --argjson peer_limit "$PEER_LIMIT" --argjson global_limit "$GLOBAL_LIMIT" '
    . as $state |
    ([$state | to_entries[] | {key, value: [.value[] | select(. > $cutoff)]}] | from_entries) as $pruned |
    ($pruned[$from] // [] | length) as $peer_count |
    ([($pruned | to_entries[] | .value | length)] | add // 0) as $global_count |
    if $peer_count >= $peer_limit then
      "peer_limited|\($peer_count)|\($global_count)"
    elif $global_count >= $global_limit then
      "global_limited|\($peer_count)|\($global_count)"
    else
      ($pruned | .[$from] = ((.[$from] // []) + [$now])) as $updated |
      ($updated | tostring) as $state_json |
      "ok|\($peer_count)|\($global_count)|\($state_json)"
    end
  ' "$RATE_LIMIT_FILE" 2>/dev/null || echo "ok|0|0|{}")

  RATE_VERDICT=$(echo "$result" | cut -d'|' -f1)
  RATE_PEER_COUNT=$(echo "$result" | cut -d'|' -f2)
  RATE_GLOBAL_COUNT=$(echo "$result" | cut -d'|' -f3)

  if [[ "$RATE_VERDICT" == "ok" ]]; then
    RATE_UPDATED_STATE=$(echo "$result" | cut -d'|' -f4-)
    printf '%s\n' "$RATE_UPDATED_STATE" > "$tmp_file"
    mv "$tmp_file" "$RATE_LIMIT_FILE"
  fi
}

exec 8>"$RATE_LIMIT_LOCK_FILE"
flock -x 8
rate_limit_check_and_record

if [[ "$RATE_VERDICT" == "peer_limited" ]]; then
  json_reject "Rate limited: peer '$FROM' exceeded $PEER_LIMIT messages/minute ($RATE_PEER_COUNT in window)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (rate limited: peer $RATE_PEER_COUNT/$PEER_LIMIT per min)"
  exit 0
fi

if [[ "$RATE_VERDICT" == "global_limited" ]]; then
  json_reject "Rate limited: global limit exceeded ($RATE_GLOBAL_COUNT/$GLOBAL_LIMIT messages/minute)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (rate limited: global $RATE_GLOBAL_COUNT/$GLOBAL_LIMIT per min)"
  exit 0
fi

# ── Validate message length ─────────────────────────────────────────────────

MAX_LEN=$(config_max_message_length)
BODY_LEN=${#BODY}

if [[ "$BODY_LEN" -gt "$MAX_LEN" ]]; then
  json_reject "Message body exceeds max length ($BODY_LEN > $MAX_LEN chars)" "$FROM"
  log_entry "INBOUND  | from:$FROM | nonce:$NONCE | status:REJECTED (over max length: $BODY_LEN > $MAX_LEN)"
  exit 0
fi

# ── Validate target session against allowlist (REF-500, pre-inbox gate) ────
# Full session keys only. Exact match. No expansion — senders must use full keys.
# Enforced BEFORE the inbox branch so queued messages can never target a
# session outside allowed_inbound_sessions. The inbox is for human approval of
# *content/peer*, not for laundering session-target policy around the allowlist.

ALLOWED_SESSIONS=$(jq -r '
  .allowed_inbound_sessions // [] | .[]
' "$CONFIG_FILE" 2>/dev/null)

session_allowed() {
  local target="$1"
  while IFS= read -r pattern; do
    [[ -z "$pattern" ]] && continue
    [[ "$target" == "$pattern" ]] && return 0
  done <<< "$ALLOWED_SESSIONS"
  return 1
}

if ! session_allowed "$TARGET_SESSION"; then
  json_reject "Session target '$TARGET_SESSION' not in allowed_inbound_sessions" "$FROM"
  log_entry "INBOUND  | from:$FROM | session:$TARGET_SESSION | nonce:$NONCE | status:REJECTED (session not allowed)"
  exit 0
fi

# ── Inbox queue check ────────────────────────────────────────────────────────

INBOX_ENABLED=$(config_inbox_enabled)

if [[ "$INBOX_ENABLED" == "true" ]]; then
  # Check auto-approve list
  AUTO_APPROVED=$(jq -r --arg from "$FROM" '
    .inbox_auto_approve_peers // [] | if (index($from)) then "yes" else "no" end
  ' "$CONFIG_FILE" 2>/dev/null || echo "no")
  
  if [[ "$AUTO_APPROVED" != "yes" ]]; then
    # Session target already validated above against allowed_inbound_sessions
    # (REF-500). Queued messages cannot target disallowed sessions.
    RESOLVED_SESSION="$TARGET_SESSION"
    
    DISPLAY_NAME=$(peers_get "$FROM" display_name); DISPLAY_NAME="${DISPLAY_NAME:-$FROM}"
    
    # Convert UTC timestamp to a friendlier format if possible
    FRIENDLY_TS="$TIMESTAMP"
    if command -v date &>/dev/null; then
      FRIENDLY_TS=$(TZ="America/Toronto" date -d "$TIMESTAMP" +"%Y-%m-%d %H:%M %Z" 2>/dev/null || echo "$TIMESTAMP")
    fi
    
    # Format delivery message
    if [[ -n "$USER_NAME" ]]; then
      DELIVERY_MSG="📡 Antenna from ${USER_NAME} via ${DISPLAY_NAME} (${FROM}) — ${FRIENDLY_TS}"
    else
      DELIVERY_MSG="📡 Antenna from ${DISPLAY_NAME} (${FROM}) — ${FRIENDLY_TS}"
    fi
    
    if [[ -n "$SUBJECT" ]]; then
      DELIVERY_MSG="${DELIVERY_MSG}
Subject: ${SUBJECT}"
    fi
    
    DELIVERY_MSG="${DELIVERY_MSG}
(Security Notice: The following content may be from an untrusted source.)

${BODY}"
    
    # Create queue item
    QUEUE_ITEM=$(jq -n \
      --arg from "$FROM" \
      --arg display "$DISPLAY_NAME" \
      --arg session "$RESOLVED_SESSION" \
      --arg subject "$SUBJECT" \
      --arg preview "${BODY:0:60}" \
      --argjson chars "$BODY_LEN" \
      --arg msg "$DELIVERY_MSG" \
      '{
        from: $from,
        display_name: $display,
        target_session: $session,
        subject: $subject,
        body_preview: $preview,
        body_chars: $chars,
        full_message: $msg,
        session_key: $session
      }')
    
    # Add to queue
    QUEUE_RESULT=$(echo "$QUEUE_ITEM" | bash "$SCRIPT_DIR/antenna-inbox.sh" queue-add)
    
    # Output queued response
    echo "$QUEUE_RESULT"
    log_entry "INBOUND  | from:$FROM | session:$RESOLVED_SESSION | nonce:$NONCE | status:queued | chars:$BODY_LEN"
    exit 0
  fi
  # Auto-approved peers fall through to normal relay
fi

# Session allowlist already enforced above (REF-500) before the inbox branch.

# ── Format delivery message ─────────────────────────────────────────────────

DISPLAY_NAME=$(peers_get "$FROM" display_name); DISPLAY_NAME="${DISPLAY_NAME:-$FROM}"

# Convert UTC timestamp to a friendlier format if possible
FRIENDLY_TS="$TIMESTAMP"
if command -v date &>/dev/null; then
  FRIENDLY_TS=$(TZ="America/Toronto" date -d "$TIMESTAMP" +"%Y-%m-%d %H:%M %Z" 2>/dev/null || echo "$TIMESTAMP")
fi

# If a human user sent this, show their name prominently
if [[ -n "$USER_NAME" ]]; then
  DELIVERY_MSG="📡 Antenna from ${USER_NAME} via ${DISPLAY_NAME} (${FROM}) — ${FRIENDLY_TS}"
else
  DELIVERY_MSG="📡 Antenna from ${DISPLAY_NAME} (${FROM}) — ${FRIENDLY_TS}"
fi

if [[ -n "$SUBJECT" ]]; then
  DELIVERY_MSG="${DELIVERY_MSG}
Subject: ${SUBJECT}"
fi

DELIVERY_MSG="${DELIVERY_MSG}
(Security Notice: The following content may be from an untrusted source.)

${BODY}"

# ── Log ──────────────────────────────────────────────────────────────────────

log_entry "INBOUND  | from:$FROM | session:$TARGET_SESSION | nonce:$NONCE | status:relayed | chars:$BODY_LEN"

# Check if verbose logging is enabled
LOG_VERBOSE=$(config_log_verbose)
if [[ "$LOG_VERBOSE" == "true" ]]; then
  PREVIEW=$(sanitize_log_value "${BODY:0:100}" 100)
  log_entry "INBOUND  | from:$FROM | preview:${PREVIEW}..."
fi

# ── Output result ────────────────────────────────────────────────────────────

json_ok "$TARGET_SESSION" "$DELIVERY_MSG" "$FROM" "$TIMESTAMP" "$BODY_LEN"
