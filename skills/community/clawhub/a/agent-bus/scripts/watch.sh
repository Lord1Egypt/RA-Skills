#!/bin/bash
# watch.sh — Agent Bus lightweight commit detection script
#
# How it works:
#   1. Use git ls-remote to get the latest remote commit SHA (pure bash, zero token cost)
#   2. Compare with the last recorded SHA
#   3. Changes detected: git pull to sync, trigger one-shot LLM cron to read messages and notify owner
#   4. No changes: exit within 1s, zero token cost

# Config (edit after installation)
MY_AGENT_ID="${AGENT_BUS_AGENT_ID:-your-agent-id}"   # Your agent ID
AGENT_BUS_REPO="${AGENT_BUS_REPO:-~/agent-bus-repo}"  # Bus repo path
OWNER_NOTIFY_TARGET="${AGENT_BUS_NOTIFY_TARGET:-}"     # Notify target (openclaw channel target)
OWNER_NOTIFY_CHANNEL="${AGENT_BUS_NOTIFY_CHANNEL:-}"   # Notify channel (e.g. daxiang)

REPO="$AGENT_BUS_REPO"
STATE_FILE=~/.openclaw/workspace/tmp/agent_bus_watch_state.json
LOCK_FILE=/tmp/agent_bus_watch.lock

# File lock to prevent concurrent runs
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "[agent-bus-watch] already running, skip"; exit 0; }

# Get the latest remote commit SHA
REMOTE_SHA=$(git -C "$REPO" ls-remote origin HEAD 2>/dev/null | awk '{print $1}')
if [[ -z "$REMOTE_SHA" ]]; then
  echo "[agent-bus-watch] ERROR: failed to get remote SHA"
  exit 1
fi

# Read the last recorded SHA
LAST_SHA=""
if [[ -f "$STATE_FILE" ]]; then
  LAST_SHA=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('lastSha',''))" 2>/dev/null || echo "")
fi

NOW=$(date +%s)
NOW_STR=$(date '+%Y-%m-%d %H:%M:%S')

# Compare
if [[ "$REMOTE_SHA" == "$LAST_SHA" ]]; then
  # No new commit, exit silently (zero token)
  exit 0
fi

# New commit detected
echo "[agent-bus-watch] $NOW_STR new commit detected: $LAST_SHA => $REMOTE_SHA"

# Immediately pull to ensure local sync
git -C "$REPO" pull origin main --no-rebase -q 2>&1 \
  || (git -C "$REPO" fetch origin main -q && git -C "$REPO" reset --hard origin/main -q) 2>&1
echo "[agent-bus-watch] pulled latest commits"

# Update state (record first to prevent duplicate triggers)
python3 - << 'PYEOF'
import json, os
import subprocess
data = {}
sf = os.path.expanduser('~/.openclaw/workspace/tmp/agent_bus_watch_state.json')
remote_sha = subprocess.check_output(['bash','-c','echo $REMOTE_SHA']).decode().strip() or 'unknown'
import time
data = {'lastSha': remote_sha, 'lastDetectedAt': int(time.time())}
json.dump(data, open(sf, 'w'), indent=2)
PYEOF
python3 -c "
import json, sys
data = {'lastSha': sys.argv[1], 'lastDetectedAt': int(sys.argv[2]), 'lastDetectedStr': sys.argv[3]}
json.dump(data, open(sys.argv[4], 'w'), indent=2)
" "$REMOTE_SHA" "$NOW" "$NOW_STR" "$STATE_FILE"

# Store the LLM prompt in a temp file to avoid quoting issues
PROMPT_FILE=$(mktemp /tmp/agent_bus_prompt.XXXXXX)
cat > "$PROMPT_FILE" << 'PROMPT_EOF'
[CONSTRAINT] Do NOT sessions_spawn. Complete all steps sequentially in this session.

You are the local agent (ID: ${MY_AGENT_ID}). Agent Bus has new messages. Execute the following full workflow:

## Step 1: Sync repo
cd ${REPO} && git pull origin main --no-rebase -q 2>/dev/null || true

## Step 2: Find unread message files
Run this bash snippet to find actionable messages (unread OR missing status field):
python3 -c "
import os, glob
inbox = 'inbox/\${MY_AGENT_ID}/'
results = []
for f in glob.glob(inbox + '*.md'):
    if '.gitkeep' in f: continue
    txt = open(f).read()
    lines = txt.split('
')
    status = ''
    for l in lines:
        if l.startswith('status:'):
            status = l.split(':',1)[1].strip()
            break
    if status in ('unread', ''):
        results.append(f)
for r in results: print(r)
" 2>/dev/null
If the output is empty, output 'Agent Bus: no new messages' and stop.
These are your unread files to process.

## Step 3: Process each unread message -- route by type

For each unread file, do the following:

### 3a. Read the message
Extract from the YAML front-matter:
- type   (task | notify | reply)
- from   (sender agent ID)
- subject
Read the full message body (everything after the front-matter --- delimiter).

### 3b. Ack the message (mark as read, commit, push)
# ack: replace 'status: unread' -> 'status: read', or insert 'status: read' if missing
python3 -c "
import re
f = '<file-path>'
txt = open(f).read()
if re.search(r'^status:', txt, re.MULTILINE):
    txt = re.sub(r'^status:.*', 'status: read', txt, flags=re.MULTILINE)
else:
    txt = re.sub(r'^(pair_ref:.*
)', r'status: read
', txt, flags=re.MULTILINE)
    if 'status: read' not in txt:
        txt = txt.replace('---
', 'status: read
---
', 1)
open(f, 'w').write(txt)
"
git -C ${REPO} add <file-path>
git -C ${REPO} commit -m 'ack: <filename>'
git -C ${REPO} push origin main --no-rebase 2>&1 || (git -C ${REPO} pull origin main --no-rebase -q && git -C ${REPO} push origin main)

### 3c. Route by type

**If type=task or type=notify:**
- Execute the task described in the message body (search / organize / analyze / answer etc.)
- Produce a result summary
- Send a reply to the sender:
    export AGENT_BUS_REPO=${REPO}
    cd ${REPO}
    bash agent-bus.sh send <from> reply "<task-result-or-confirmation>"
- Notify owner via message tool:
    channel: ${OWNER_NOTIFY_CHANNEL}
    target: ${OWNER_NOTIFY_TARGET}
    content: [Agent Bus] From: <from> | task: <first 80 chars of body> | result: <summary> | replied: done

**If type=reply:**
- Do NOT execute as a new task -- this is an inbound reply from another agent.
- Find the active main agent session key with this bash snippet (run it):

MAIN_SESSION=$(python3 -c "
import os, glob, json
d = '/mnt/openclaw/.openclaw/agents/main/sessions'
files = [(os.path.getmtime(f), os.path.getsize(f), f) for f in glob.glob(d + '/*.jsonl')]
files.sort(reverse=True)
for mtime, size, f in files:
    if size < 10240: continue
    try:
        with open(f) as fp: first = fp.readline()
        msg = json.loads(first)
        content = str(msg.get('message', {}).get('content', ''))
        if 'cron:' in content: continue
    except: pass
    print(os.path.basename(f).replace('.jsonl', ''))
    break
")

- Inject the reply into the main session:
    openclaw agent --session-id "$MAIN_SESSION" --deliver --channel ${OWNER_NOTIFY_CHANNEL} --reply-to ${OWNER_NOTIFY_TARGET} -m "[Agent Bus Reply] From: <from>

<FULL message body>

Please process this reply and decide next steps."

- Notify owner via message tool:
    channel: ${OWNER_NOTIFY_CHANNEL}
    target: ${OWNER_NOTIFY_TARGET}
    content: [Agent Bus Reply] From: <from> | subject: <subject> | Main session woken up for orchestration.

## Notes
- Process ALL unread files before stopping
- If web search is needed for a task, use the web_fetch tool
- Do NOT sessions_spawn
PROMPT_EOF

# Trigger LLM one-shot cron to read messages and notify owner
echo "[agent-bus-watch] triggering LLM cron to read and notify..."
openclaw cron add \
  --name "agent-bus-notify" \
  --at "1m" \
  --session isolated \
  --message "$(cat "$PROMPT_FILE")" \
  --channel "${OWNER_NOTIFY_CHANNEL}" \
  --to "${OWNER_NOTIFY_TARGET}" \
  --announce \
  2>/dev/null || true

rm -f "$PROMPT_FILE"
echo "[agent-bus-watch] done"
