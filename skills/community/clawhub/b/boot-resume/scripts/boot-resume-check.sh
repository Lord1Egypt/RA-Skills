#!/usr/bin/env bash
# boot-resume-check.sh — Deterministic interrupted-session detector.
# Run as ExecStartPost in openclaw-gateway.service, or manually via /boot-resume.
# Scans all active sessions; if a session was interrupted mid-turn
# (last entry is user message, toolResult, or empty assistant),
# schedules a one-shot system-event via `openclaw cron add` to auto-resume.
set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
WINDOW_MINUTES=20
DELAY="20s"
LOG_TAG="[boot-resume]"
CANDIDATES_FILE=$(mktemp /tmp/boot-resume-candidates.XXXXXX)
trap 'rm -f "$CANDIDATES_FILE"' EXIT

# Log rotation: keep last 500 lines
LOG_FILE="/tmp/openclaw/boot-resume.log"
mkdir -p /tmp/openclaw
if [[ -f "$LOG_FILE" ]] && [[ $(wc -l < "$LOG_FILE") -gt 1000 ]]; then
  tail -500 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

log() { echo "$(date +%Y-%m-%dT%H:%M:%S%z) $LOG_TAG $*"; }

# Skip startup sleep if invoked manually (not from systemd ExecStartPost)
if [[ "${1:-}" == "--no-wait" ]]; then
  log "manual invocation (--no-wait)"
else
  # Wait for gateway to be ready (needs to accept cron add commands)
  sleep 12
fi

# Auto-discover agent directories
AGENTS_DIR="$OPENCLAW_HOME/agents"
if [[ ! -d "$AGENTS_DIR" ]]; then
  log "agents directory not found at $AGENTS_DIR, skipping"
  exit 0
fi

NOW_MS=$(date +%s%3N 2>/dev/null || python3 -c "import time; print(int(time.time()*1000))")
CUT_MS=$(( NOW_MS - WINDOW_MINUTES * 60 * 1000 ))

log "now=$NOW_MS cut=$CUT_MS (${WINDOW_MINUTES}min window)"

# Collect session keys already handled by restart-resume.json
RESUME_JSON="$OPENCLAW_HOME/workspace/state/restart-resume.json"
HANDLED_KEY=""
if [[ -f "$RESUME_JSON" ]]; then
  PENDING=$(python3 -c "import json; d=json.load(open('$RESUME_JSON')); print(d.get('pending',''))" 2>/dev/null || echo "")
  if [[ "$PENDING" == "True" || "$PENDING" == "true" ]]; then
    HANDLED_KEY=$(python3 -c "import json; d=json.load(open('$RESUME_JSON')); print(d.get('sessionKey',''))" 2>/dev/null || echo "")
  fi
fi

# Scan all agents (support multi-agent deployments)
for AGENT_DIR in "$AGENTS_DIR"/*/; do
  SESSIONS_INDEX="${AGENT_DIR}sessions/sessions.json"
  if [[ ! -f "$SESSIONS_INDEX" ]]; then
    continue
  fi

  AGENT_ID=$(basename "$AGENT_DIR")
  log "scanning agent: $AGENT_ID"

  # Parse sessions.json and find candidates
  if ! python3 - "$SESSIONS_INDEX" "$CUT_MS" "$HANDLED_KEY" > "$CANDIDATES_FILE" 2>&1 <<'PYEOF'
import json, sys, os

index_path = sys.argv[1]
cut_ms = int(sys.argv[2])
handled_key = sys.argv[3] if len(sys.argv) > 3 else ""

with open(index_path) as f:
    sessions = json.load(f)

for key, meta in sessions.items():
    # Skip system, heartbeat, cron, and subagent sessions
    if key.endswith(":main") or "heartbeat" in key:
        continue
    if ":cron:" in key or ":subagent:" in key:
        continue
    # Skip already handled by restart-resume.json
    if handled_key and key == handled_key:
        continue
    # Check recency
    updated_at = meta.get("updatedAt", 0)
    if updated_at < cut_ms:
        continue
    session_file = meta.get("sessionFile", "")
    if not session_file or not os.path.isfile(session_file):
        continue
    session_id = meta.get("sessionId", "")
    print(f"{key}\t{session_id}\t{session_file}")
PYEOF
  then
    log "ERROR: failed to parse $SESSIONS_INDEX"
    cat "$CANDIDATES_FILE" | while read -r errline; do log "  $errline"; done
    truncate -s 0 "$CANDIDATES_FILE"
    continue
  fi

  # Filter: remove lines that look like error output (not tab-separated)
  grep -P '\t' "$CANDIDATES_FILE" > "${CANDIDATES_FILE}.filtered" 2>/dev/null && mv "${CANDIDATES_FILE}.filtered" "$CANDIDATES_FILE" || true

  CANDIDATE_COUNT=$(wc -l < "$CANDIDATES_FILE" | tr -d ' ')
  log "candidates: $CANDIDATE_COUNT (agent=$AGENT_ID)"

  if [[ "$CANDIDATE_COUNT" -eq 0 ]]; then
    continue
  fi

  while IFS=$'\t' read -r SESSION_KEY SESSION_ID SESSION_FILE; do
    log "checking: $SESSION_KEY ($SESSION_ID)"

    # Read last 5 lines of JSONL, determine if session was interrupted.
    STATUS=$(tail -5 "$SESSION_FILE" | python3 -c "
import sys, json, re

last_type = ''
last_text = ''

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        msg = d.get('message', {})
        role = msg.get('role', '')

        if role == 'toolResult':
            last_type = 'toolResult'
        elif role == 'user':
            last_type = 'user'
            content = msg.get('content', '')
            if isinstance(content, list):
                texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                last_text = ' '.join(texts)
            else:
                last_text = str(content)
        elif role == 'assistant':
            last_type = 'assistant'
            content = msg.get('content', '')
            if isinstance(content, list):
                texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                last_text = ' '.join(texts)
            else:
                last_text = str(content)
    except Exception as e:
        print(f'PARSE_ERROR:{e}', file=sys.stderr)

if last_type == 'toolResult':
    print('INTERRUPTED')
elif last_type == 'assistant':
    if len(last_text.strip()) == 0:
        print('INTERRUPTED')
    else:
        print('COMPLETE')
elif last_type == 'user':
    # Strip OpenClaw metadata blocks (Conversation info / Sender)
    clean = re.sub(r'(?:Conversation info|Sender) \(untrusted metadata\):\s*\x60{3}json\s*.*?\x60{3}\s*', '', last_text, flags=re.DOTALL).strip()
    trivial = {'ok', 'yes', 'no', 'thanks', 'thx', 'sure', 'got it', 'noted'}
    is_trivial = clean.lower() in trivial or (len(clean) <= 2 and not clean.isalnum())
    if not is_trivial and len(clean) > 0:
        print('INTERRUPTED')
    else:
        print('TRIVIAL')
else:
    print('EMPTY')
" 2> >(while read -r errline; do log "  python: $errline"; done))

    # Handle empty STATUS (python crash)
    if [[ -z "$STATUS" ]]; then
      log "WARNING: empty status for $SESSION_KEY, skipping"
      continue
    fi

    log "status: $SESSION_KEY -> $STATUS"

    if [[ "$STATUS" != "INTERRUPTED" ]]; then
      log "skip $SESSION_KEY ($STATUS)"
      continue
    fi

    SHORT_ID="${SESSION_ID:0:8}"
    TIMESTAMP=$(date +%s)
    JOB_NAME="boot-resume-${SHORT_ID}-${TIMESTAMP}"
    log "INTERRUPTED: $SESSION_KEY — scheduling resume as $JOB_NAME"

    openclaw cron add \
      --name "$JOB_NAME" \
      --session "$AGENT_ID" \
      --session-key "$SESSION_KEY" \
      --at "$DELAY" \
      --system-event "The gateway just restarted. The conversation above was interrupted mid-turn. Continue fulfilling the user's last request as if no interruption occurred. Respond in the same language the user was using." \
      --delete-after-run \
      --wake now \
      --json 2> >(while read -r errline; do log "  cron-add: $errline"; done) \
      && log "resume armed for $SESSION_KEY" \
      || log "ERROR: cron add failed for $SESSION_KEY"

  done < "$CANDIDATES_FILE"

done

log "done"
