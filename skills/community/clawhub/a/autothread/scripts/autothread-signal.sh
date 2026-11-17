# autothread-signal.sh — Signal adapter for /topic (pseudo-topic mode).
#
# DISCLOSURE: this script reads the local OpenClaw config (bot/Signal
# credentials only) and sends message content, sender attribution and
# the target group/number to Signal via the local signal-cli daemon
# socket, or directly via the signal-cli CLI when no daemon runs.
# Nothing is sent anywhere else. See SKILL.md "Privacy & data handling".
#
# IMPORTANT LIMITATION: Signal has no native forum topics or threads.
# There is no bot API object equivalent to a Telegram forum topic or a
# Discord thread. This adapter therefore runs in "pseudo-topic" mode:
#
#   1. It posts a titled, quoted digest of the original message to the
#      same group, using a distinctive header so digest messages are
#      recognisable and searchable ("📌 <title>").
#   2. It returns the *sent timestamp* as the topic_id (Signal's only
#      stable message identifier) and link=null.
#
# Targets: the first argument may be either a GROUP ID (as returned by
# `signal-cli listGroups`) or a phone number starting with "+". Phone
# numbers send a direct message — "+<your own number>" delivers to
# Note to Self.
#
# Usage:
#   ./autothread-signal.sh <group_id_or_phone> <timestamp> <sender> [title] [text]
#
# Args:
#   target    (required) — group ID, or phone number (+1234…) for DMs;
#                          your own number delivers to Note to Self
#   timestamp (required) — timestamp of the original message (digits);
#                          used for reference only, messages cannot be
#                          quoted programmatically without signal-cli
#                          receive state.
#   sender    (required) — display name of the original sender
#   title     (optional) — pseudo-topic title (fallback auto-generated)
#   text      (optional) — message body (everything after "/topic")
#
# Prerequisites:
#   - signal-cli installed and a registered/linked account configured in
#     the OpenClaw config (.channels.signal.account).
#
# Output: JSON — {"topic_id": "<timestamp>", "title": "<title>", "link": null}
# Exit codes: 0 = success, 1 = error (details on stderr)

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

autothread_require signal-cli jq
autothread_config_path >/dev/null

# ── config ──────────────────────────────────────────────────────────
SIGNAL_ACCOUNT=$(autothread_config_get '.channels.signal.account // empty')

# ── daemon detection ────────────────────────────────────────────────
# When a signal-cli daemon is running for this user, direct CLI `send`
# invocations conflict with the daemon's account lock (they hang). The
# daemon exposes a JSON-RPC socket instead; sends go through it (fast,
# no lag). When no daemon runs, fall back to direct CLI sends.
RPC_SOCKET="/run/user/$(id -u)/signal-cli/socket"
USE_RPC=0
if [ -S "$RPC_SOCKET" ] && command -v python3 &>/dev/null; then
  USE_RPC=1
fi

# ── arguments ───────────────────────────────────────────────────────
TARGET="${1:-}"
TIMESTAMP="${2:-}"
SENDER="${3:-}"
TITLE_ARG="${4:-}"
RAW_TEXT="${5:-}"

if [ -z "$TARGET" ] || [ -z "$TIMESTAMP" ] || [ -z "$SENDER" ]; then
  echo "Usage: $0 <group_id_or_phone> <timestamp> <sender> [title] [text]" >&2
  exit 1
fi

if ! printf '%s' "$TIMESTAMP" | grep -qE '^[0-9]+$'; then
  echo "ERROR: timestamp must be a positive integer (Signal epoch ms), got: '$TIMESTAMP'" >&2
  exit 1
fi

MSG=$(autothread_trim "$RAW_TEXT")

# ── resolve the target: group ID or phone number (DM) ───────────────
# Phone numbers start with "+" and send direct messages (Note to Self
# when the number is the account's own). Everything else is treated as
# a group ID.
SEND_ARGS=()
KIND="group"
if printf '%s' "$TARGET" | grep -qE '^\+[0-9][0-9 ()-]*[0-9]$'; then
  SEND_ARGS=("$TARGET")
  KIND="dm"
else
  SEND_ARGS=(-g "$TARGET")
fi

# ── determine title ─────────────────────────────────────────────────
if [ -n "$TITLE_ARG" ]; then
  TITLE="$TITLE_ARG"
else
  TITLE=$(autothread_fallback_title "$MSG")
fi
# Signal caps outgoing messages well above 128 chars, but keep titles
# short and consistent with the other adapters.
TITLE=$(printf '%s' "$TITLE" | cut -c1-128)

# ── compose the pseudo-topic digest ─────────────────────────────────
# Multi-line message body sent via signal-cli. There is no quote API,
# so the digest restates the content with attribution.
BODY="📌 ${TITLE}
────────────────
${MSG}
────────────────
— ${SENDER} (via /topic)"

# ── send ────────────────────────────────────────────────────────────
# DM  → JSON-RPC "recipient"; group → JSON-RPC "groupId".
# Direct CLI fallback: positional recipient for DMs, -g for groups.
SENT_OUTPUT=""
if [ "$USE_RPC" -eq 1 ]; then
  if [ "$KIND" = "dm" ]; then
    RPC_PARAMS=$(jq -n --arg a "$SIGNAL_ACCOUNT" --arg r "$TARGET" --arg m "$BODY" \
      '{account: $a, recipient: $r, message: $m}')
  else
    RPC_PARAMS=$(jq -n --arg a "$SIGNAL_ACCOUNT" --arg g "$TARGET" --arg m "$BODY" \
      '{account: $a, groupId: $g, message: $m}')
  fi
  SENT_OUTPUT=$(TARGET_SOCK="$RPC_SOCKET" RPC_PARAMS="$RPC_PARAMS" python3 - <<'PYEOF'
import socket, json, os
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(30)
s.connect(os.environ["TARGET_SOCK"])
req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "send", "params": json.loads(os.environ["RPC_PARAMS"])})
s.sendall((req + "\n").encode())
buf = b""
try:
    while "\n" not in buf.decode(errors="ignore"):
        c = s.recv(65536)
        if not c:
            break
        buf += c
except socket.timeout:
    pass
line = buf.decode(errors="ignore").strip().splitlines()[0] if buf.strip() else "{}"
resp = json.loads(line)
if "error" in resp:
    print("RPCERROR " + json.dumps(resp["error"]))
else:
    ts = resp.get("result", {}).get("timestamp", "")
    print(str(ts))
PYEOF
)
  if printf '%s' "$SENT_OUTPUT" | grep -q '^RPCERROR'; then
    echo "ERROR: signal-cli JSON-RPC send failed: $SENT_OUTPUT" >&2
    exit 1
  fi
  SENT_STATUS=0
else
  SENT_OUTPUT=$(signal-cli -u "$SIGNAL_ACCOUNT" send "${SEND_ARGS[@]}" -m "$BODY" 2>&1)
  SENT_STATUS=$?
fi

if [ "$SENT_STATUS" -ne 0 ]; then
  echo "ERROR: signal-cli send failed: ${SENT_OUTPUT}" >&2
  exit 1
fi

# The sent timestamp(s) become the topic id; fall back to the original
# message timestamp when unavailable.
SENT_TS=$(printf '%s' "$SENT_OUTPUT" | grep -oE '^[0-9]{13,}$' | tail -1)
TOPIC_ID="${SENT_TS:-$TIMESTAMP}"

# No shareable link concept in Signal
autothread_emit_result "$TOPIC_ID" "$TITLE" ""
