#!/usr/bin/env bash
# delivery-mirror — send a Telegram (or other channel) message via OpenClaw AND
# mirror the delivered text into the target session transcript, so the agent that
# "owns" that chat/topic sees the message in its own context on the next turn.
#
# WHY: `--command` crons and external scripts that call `openclaw message send`
# bypass the agent's run loop. The message reaches the chat, but the agent's
# session JSONL never records it — the agent has no memory it was ever sent.
# This helper appends a `delivery-mirror` assistant row (the same shape the
# OpenClaw delivery layer writes via appendAssistantMessageToSessionTranscript)
# so the transcript stays continuous. No OpenClaw core changes required.
#
# Subcommand-free; flags only. Example:
#   send-mirrored.sh \
#     --agent ula --account ula \
#     --to -1003971971641 --thread-id 131 \
#     --source agenda-dispatch \
#     --message "$MSG"
#
# Exit codes:
#   0  delivered (+ mirrored, or mirror skipped as best-effort with a warning)
#   2  bad usage / missing required args / a flag is missing its value
#   3  idempotency: this --idem key was already handled, nothing done
#   4  send failed (nothing mirrored)
set -uo pipefail

# ---- defaults ---------------------------------------------------------------
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"
CHANNEL="telegram"
ACCOUNT=""
AGENT=""
TO=""
THREAD=""
MESSAGE=""
MESSAGE_FILE=""
SESSION_KEY=""
SOURCE="script"
IDEM=""
DRY=0
NO_SEND=0
NO_MIRROR=0

usage() { sed -n '2,40p' "$0"; }
die_usage() { echo "delivery-mirror: $1" >&2; exit 2; }
# Ensure a value-taking flag actually has a value (safe under `set -u`).
need_val() { [ "$#" -ge 2 ] || die_usage "$1 requires a value"; }

# ---- arg parsing ------------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --message)        need_val "$@"; MESSAGE="$2"; shift 2;;
    --message-file)   need_val "$@"; MESSAGE_FILE="$2"; shift 2;;
    --to)             need_val "$@"; TO="$2"; shift 2;;
    --channel)        need_val "$@"; CHANNEL="$2"; shift 2;;
    --account)        need_val "$@"; ACCOUNT="$2"; shift 2;;
    --agent)          need_val "$@"; AGENT="$2"; shift 2;;
    --thread-id)      need_val "$@"; THREAD="$2"; shift 2;;
    --session-key)    need_val "$@"; SESSION_KEY="$2"; shift 2;;
    --source)         need_val "$@"; SOURCE="$2"; shift 2;;
    --idem)           need_val "$@"; IDEM="$2"; shift 2;;
    --openclaw-home)  need_val "$@"; OPENCLAW_HOME="$2"; shift 2;;
    --openclaw-bin)   need_val "$@"; OPENCLAW_BIN="$2"; shift 2;;
    --dry-run)        DRY=1; shift;;
    --no-send)        NO_SEND=1; shift;;        # mirror only (testing)
    --no-mirror)      NO_MIRROR=1; shift;;      # send only (behaves like plain send)
    -h|--help)        usage; exit 0;;
    *) echo "delivery-mirror: unknown arg: $1" >&2; usage >&2; exit 2;;
  esac
done

# message may come from --message-file or stdin ("-")
if [ -n "$MESSAGE_FILE" ]; then
  if [ "$MESSAGE_FILE" = "-" ]; then MESSAGE="$(cat)"; else MESSAGE="$(cat "$MESSAGE_FILE")"; fi
fi

# ---- validation -------------------------------------------------------------
[ -n "$MESSAGE" ] || die_usage "--message (or --message-file) required"
[ -n "$TO" ]      || die_usage "--to required"
[ -n "$AGENT" ]   || die_usage "--agent required (agent id owning the session)"
[ -n "$ACCOUNT" ] || ACCOUNT="$AGENT"   # channel account defaults to agent id

STATE_DIR="$OPENCLAW_HOME/delivery-mirror/state"
LOG="$OPENCLAW_HOME/delivery-mirror/mirror.log"
SESSIONS_JSON="$OPENCLAW_HOME/agents/$AGENT/sessions/sessions.json"
mkdir -p "$STATE_DIR"
SEEN="$STATE_DIR/${AGENT}.seen"
touch "$SEEN"

log() { echo "[$(date -u +%FT%TZ)] $*" >>"$LOG" 2>/dev/null; }

# ---- idempotency: lock the whole check -> send -> mark critical section ------
# Only when --idem is used (otherwise nothing touches the seen file, so no race).
if [ -n "$IDEM" ]; then
  exec 9>"$SEEN.lock"
  flock 9                                  # released on process exit
  if grep -qxF "$IDEM" "$SEEN" 2>/dev/null; then
    log "skip idem=$IDEM source=$SOURCE (already handled)"
    echo "delivery-mirror: idem '$IDEM' already handled, nothing to do" >&2
    exit 3
  fi
fi

# ---- dry run ----------------------------------------------------------------
if [ "$DRY" = "1" ]; then
  echo "----- DRY RUN -----"
  echo "channel : $CHANNEL"
  echo "account : $ACCOUNT"
  echo "to      : $TO"
  echo "thread  : ${THREAD:-<none>}"
  echo "agent   : $AGENT"
  echo "source  : $SOURCE"
  echo "idem    : ${IDEM:-<none>}"
  echo "session : ${SESSION_KEY:-<auto-resolve>}"
  echo "no-send : $NO_SEND   no-mirror: $NO_MIRROR"
  echo "--- message ---"
  printf '%s\n' "$MESSAGE"
  exit 0
fi

# ---- 1) send ----------------------------------------------------------------
SEND_JSON=""
if [ "$NO_SEND" != "1" ]; then
  send_args=( message send --channel "$CHANNEL" --account "$ACCOUNT" -t "$TO" -m "$MESSAGE" --json )
  [ -n "$THREAD" ] && send_args+=( --thread-id "$THREAD" )
  if ! SEND_JSON="$("$OPENCLAW_BIN" "${send_args[@]}" 2>&1)"; then
    log "SEND FAIL source=$SOURCE to=$TO thread=${THREAD:-} out=${SEND_JSON//$'\n'/ }"
    echo "delivery-mirror: send failed: $SEND_JSON" >&2
    exit 4
  fi
  log "sent source=$SOURCE to=$TO thread=${THREAD:-}"
else
  log "no-send source=$SOURCE (mirror only)"
fi

# ---- 2) mirror into the session transcript (best-effort) --------------------
if [ "$NO_MIRROR" != "1" ]; then
  # Inputs are passed as positional argv (NOT environment variables): the helper
  # never reads ambient env for data, so it cannot harvest or leak unrelated
  # environment. All values below are produced by this script's own flags.
  python3 - "$SESSIONS_JSON" "$SESSION_KEY" "$CHANNEL" "$AGENT" "$TO" "$THREAD" "$MESSAGE" "$SEND_JSON" <<'PY'
import sys, json, uuid, time, fcntl

sj_path = sys.argv[1]
key     = sys.argv[2]
channel = sys.argv[3]
agent   = sys.argv[4]
to      = sys.argv[5]
thread  = sys.argv[6]
msg     = sys.argv[7]
send_js = sys.argv[8]

def warn(m): print(f"delivery-mirror: WARN mirror: {m}", file=sys.stderr)

try:
    with open(sj_path) as f:
        sessions = json.load(f)
except Exception as e:
    warn(f"cannot read sessions.json ({sj_path}): {e}; delivery ok, mirror skipped")
    sys.exit(0)

def candidate_keys():
    if key:
        yield key
        return
    if thread:
        yield f"agent:{agent}:{channel}:group:{to}:topic:{thread}"
    yield f"agent:{agent}:{channel}:group:{to}"
    yield f"agent:{agent}:{channel}:direct:{to}"

entry = None
for k in candidate_keys():
    if k in sessions:
        entry = sessions[k]; break

# fall back: match by delivery target + thread across all entries
if entry is None:
    for _k, v in sessions.items():
        if not isinstance(v, dict):
            continue
        dc = v.get("deliveryContext") or {}
        rt = (v.get("route") or {}).get("target") or {}
        dest = dc.get("to") or rt.get("to") or ""
        tid = dc.get("threadId")
        if tid is None:
            tid = (v.get("route") or {}).get("thread", {}).get("id")
        if str(to) in dest and (str(tid) == str(thread) if thread else tid in (None, "")):
            entry = v; break

if entry is None:
    warn(f"no session entry matched to={to} thread={thread or '-'}; delivery ok, mirror skipped")
    sys.exit(0)

session_file = entry.get("sessionFile")
if not session_file:
    warn("matched session has no sessionFile; delivery ok, mirror skipped")
    sys.exit(0)

# best-effort: pull the delivered message id from the send --json result
def find_message_id(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (str, int)) and k.lower() in ("messageid", "message_id"):
                return str(v)
        for v in obj.values():
            r = find_message_id(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_message_id(v)
            if r:
                return r
    return None

source_message_id = None
if send_js.strip():
    try:
        source_message_id = find_message_id(json.loads(send_js))
    except Exception:
        source_message_id = None

marker = {"kind": "channel-final"}
if source_message_id:
    marker["sourceMessageId"] = source_message_id

now_ms = int(time.time() * 1000)
iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(now_ms / 1000)) + f".{now_ms % 1000:03d}Z"

lock_path = session_file + ".mirror.lock"
try:
    lf = open(lock_path, "w")
    fcntl.flock(lf, fcntl.LOCK_EX)
except Exception as e:
    warn(f"could not acquire lock {lock_path}: {e}; delivery ok, mirror skipped")
    sys.exit(0)

try:
    # parentId + trailing-newline check must happen UNDER the lock, so two
    # concurrent mirrors can't read the same tail / clobber each other.
    parent_id = None
    needs_newline = False
    try:
        with open(session_file, "rb") as f:
            last = None
            for line in f:
                stripped = line.strip()
                if stripped:
                    last = stripped
            if last:
                try:
                    parent_id = json.loads(last).get("id")
                except Exception:
                    parent_id = None
            # if the file is non-empty and does not end in a newline, our raw
            # append would glue onto the previous record — prepend one.
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(-1, 2)
                needs_newline = f.read(1) != b"\n"
    except FileNotFoundError:
        pass
    except Exception as e:
        warn(f"could not read tail of {session_file}: {e}; appending with parentId=null")

    record = {
        "type": "message",
        "id": str(uuid.uuid4()),
        "parentId": parent_id,
        "timestamp": iso,
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": msg}],
            "api": "openai-responses",
            "provider": "openclaw",
            "model": "delivery-mirror",
            "usage": {
                "input": 0,
                "output": 0,
                "cacheRead": 0,
                "cacheWrite": 0,
                "totalTokens": 0,
                "cost": {
                    "input": 0,
                    "output": 0,
                    "cacheRead": 0,
                    "cacheWrite": 0,
                    "total": 0,
                },
            },
            "stopReason": "stop",
            "timestamp": now_ms,
            "openclawDeliveryMirror": marker,
        },
    }
    line = ("\n" if needs_newline else "") + json.dumps(record, ensure_ascii=False) + "\n"
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"delivery-mirror: mirrored into {session_file}", file=sys.stderr)
except Exception as e:
    warn(f"append failed for {session_file}: {e}; delivery ok")
finally:
    try:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()
    except Exception:
        pass
sys.exit(0)
PY
fi

# ---- 3) record idempotency key (only after the success path, still locked) ---
if [ -n "$IDEM" ]; then
  printf '%s\n' "$IDEM" >>"$SEEN"
fi

exit 0
