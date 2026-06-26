# Known Bugs & Gotchas

Every bug here was hit in production. Each one cost hours or days to diagnose.

---

## 1. Future-Dated Timestamp (THE #1 bug)

**Symptom**: Agent polls inbox, always gets 0 messages, appears completely deaf for hours/days.

**Cause**: The cursor file (`/tmp/acp_bridge_last_ts`) contains a timestamp in the future. Every poll asks "give me messages after next Tuesday" → 0 results → agent thinks it's caught up.

**How it happens**:
- Saving `id` (milliseconds) instead of `ts` (seconds) — `id` value is 1000x larger, lands years in the future
- Timezone arithmetic bugs
- Manually writing a bad value during debugging

**Diagnosis**:
```bash
LAST_TS=$(cat /tmp/acp_bridge_last_ts 2>/dev/null || echo 0)
NOW=$(python3 -c "import time; print(time.time())")
echo "Cursor: $LAST_TS | Now: $NOW"
python3 -c "
import datetime
cursor = datetime.datetime.fromtimestamp(float('$LAST_TS'))
now = datetime.datetime.now()
diff = cursor - now
print(f'Cursor points to: {cursor}')
print(f'Now: {now}')
if diff.total_seconds() > 60:
    print(f'⚠️ CURSOR IS {diff} IN THE FUTURE — this is the bug')
else:
    print('✅ Cursor is in the past (normal)')
"
```

**Fix**:
```bash
python3 -c "import time; print(time.time())" > /tmp/acp_bridge_last_ts
```

**Prevention**: Add to heartbeat:
```bash
LAST_TS=$(cat /tmp/acp_bridge_last_ts 2>/dev/null || echo 0)
NOW=$(python3 -c "import time; print(time.time())")
if python3 -c "exit(0 if float('$LAST_TS') < float('$NOW') + 60 else 1)"; then
    echo "Bridge cursor OK"
else
    echo "⚠️ FUTURE TIMESTAMP — resetting"
    echo "$NOW" > /tmp/acp_bridge_last_ts
fi
```

---

## 2. ts vs id Confusion

**Symptom**: Duplicate messages delivered, or messages skipped.

**Cause**: Messages have two time fields that look similar but aren't interchangeable:
- `ts`: `1774367583.0932004` — **float seconds** (use this for `after=`)
- `id`: `1774367583093` — **integer milliseconds** (unique ID only)

Dividing `id / 1000` introduces floating-point rounding errors → cursor lands between messages → duplicates or gaps.

**Rule**: Always extract and save the `ts` field. Never do math on `id`. The `save_bridge_ts.sh` script handles both formats as a safety net, but always prefer passing `ts` directly.

---

## 3. Newlines in curl Break JSON

**Symptom**: `JSONDecodeError` on bridge server when sending multi-line messages.

**Cause**: Shell interpolation of newlines inside `curl -d '...'` produces invalid JSON.

```bash
# BROKEN — newlines inside single quotes break JSON parsing
curl -d '{"message": "line 1
line 2"}'

# ALSO BROKEN — \n not escaped properly
curl -d '{"message": "line 1\nline 2"}'
```

**Fix**: Always use `bridge_reply.py` for replies. For sends, use python:
```bash
python3 -c "
import json, urllib.request
msg = '''Your multi-line
message here'''
data = json.dumps({'message': msg, 'from': 'agent_a'}).encode()
req = urllib.request.Request('http://localhost:18790/api/send',
    data=data, headers={'Authorization': 'Bearer TOKEN', 'Content-Type': 'application/json'})
urllib.request.urlopen(req)
"
```

---

## 4. Context Loss Between Poll Cycles

**Symptom**: Agent acknowledges a task in one poll cycle, completely forgets it in the next. Acknowledge → forget → acknowledge loop forever.

**Cause**: Each cron poll spawns an isolated session with zero memory of previous polls. The agent has no persistent state.

**Fix**: WAL (Write-Ahead Log) protocol:
1. Create a `SESSION-STATE.md` file in the workspace (acts as "hot RAM")
2. Cron prompt instructs the agent to read SESSION-STATE.md FIRST
3. Before responding, agent writes current state to SESSION-STATE.md
4. Next cycle reads it and picks up where it left off

**Key rule**: Write state BEFORE responding, not after. If the agent crashes after responding but before saving → lost context (catastrophic). If it crashes after saving but before responding → lost reply (recoverable). Always choose the recoverable failure mode.

---

## 5. Stale Follow-Up Spam

**Symptom**: Sending agent fires "task pending > 60 min, deliver update" every hour. Receiving agent processes each as a new task, burns tokens composing responses to each nudge.

**Cause**: Automated follow-up cron on the sender side that doesn't know the receiver already handled the task.

**Fix**: Add to receiver's cron prompt:
```
Skip messages matching 'Follow-up: These tasks have been pending' — instead,
check if the underlying task is actually done and report that.
```

Also consider: make the sender smarter — check outbox for replies before nagging.

---

## 6. Model Too Weak for Substantive Replies

**Symptom**: Agent polls inbox, reads a complex multi-step task, responds with:
- "Acknowledged, forwarding to main session"
- "Standing by for further instructions"
- HEARTBEAT_OK
- Any variation of "I'll get back to you"

**Cause**: Using a cheap/fast model (MiniMax, Haiku, GPT-4o-mini) that lacks the capability to execute multi-step tasks with tool calls.

**Fix**: The bridge poll cron IS the agent's brain for that cycle. Use a capable model:
- Anthropic: `claude-opus-4-6` or `claude-sonnet-4-5`
- OpenAI: `gpt-4o` or `o1`
- Don't use mini/lite models for bridge relay

**Cost concern?** Use a strong model for the poll cron but keep maintenance crons (backup, pruning, logging) on cheap models.

---

## 7. JSONL Files Grow Forever

**Symptom**: Bridge server starts responding slowly after weeks. High disk usage in bridge directory.

**Cause**: `inbox.jsonl` and `outbox.jsonl` are append-only. Every message ever sent accumulates. After months of 10-min polling with substantive messages, files reach 50-100MB+. Every poll reads the entire file to filter by timestamp.

**Fix**: Run `scripts/bridge_prune.py` weekly:
```bash
python3 bridge_prune.py --days 7 --dir /tmp/acp_bridge
```

Or add a cron job (see `cron-templates.md` for the template).

---

## 8. Bridge Server Dies Silently

**Symptom**: Both agents stop communicating. No errors in agent logs because curl returns connection refused and the cron prompt handles "count == 0" as "no new messages."

**Cause**: Bridge Python process crashed (OOM, unhandled exception, machine reboot) and nobody noticed.

**Fix**: Heartbeat checks bridge health endpoint. Add process keepalive to supervisor:
```bash
# In startup script or cron
if ! curl -s -f http://localhost:18790/api/health > /dev/null 2>&1; then
    echo "Bridge down — restarting"
    nohup python3 /path/to/acp_bridge.py > /tmp/acp_bridge.log 2>&1 &
    echo $! > /tmp/acp_bridge.pid
fi
```
