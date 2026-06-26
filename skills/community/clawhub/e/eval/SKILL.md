---
name: eval
description: "Evaluate everything the PA agent manages — tasks, skills, PA network health, billing, calendar connections, and memory quality. Use when: owner asks for an evaluation, wants to know what's working and what isn't, or requests a performance report. Combines supervisor status with quality scoring."
---

## Load Local Context
```bash
CONTEXT_FILE="/opt/ocana/openclaw/workspace/skills/eval/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $OWNER_PHONE, $WORKSPACE, $TASKS_FILE, $MONDAY_TOKEN_FILE, $GOG_CREDS, etc.
```

# Eval Skill

Structured evaluation of everything the agent manages.

---

## When to Use

Trigger phrases:
- "run eval"
- "what's working and what isn't"
- "rate yourself"
- "check everything"

## Pre-Eval Behavioral Checks (Always)
1. React 👍 when owner triggers eval
2. React ✅ when report is complete
3. PA directory source: `/opt/ocana/openclaw/workspace/PA_LIST.md`
4. Calendar check: use direct API (NOT gog CLI)

---

## Eval Report Format

```
📋 Full Eval — [DATE]

━━━ SELF PERFORMANCE ━━━
Execution:      [1-5] [comment]
Accuracy:       [1-5] [comment]
Memory:         [1-5] [comment]
Proactivity:    [1-5] [comment]
Communication:  [1-5] [comment]
TOTAL: [X]/25

━━━ ACTIVE TASKS ━━━
✅ Done today:   [count]
🟡 In progress:  [count]
❌ Stalled:      [count] — [list stalled tasks]

━━━ PA NETWORK ━━━
✅ Working:  [list]
⚠️ Issues:   [list with issue]
❌ Down:     [list]

━━━ SKILLS ━━━
Installed: [count]
Used today: [list]
Unused (7+ days): [list]

━━━ INTEGRATIONS ━━━
Calendar (owner):     [connected ✅ / broken ❌ / unknown ?]
monday.com:           [connected ✅ / broken ❌]
Email (gog):          [connected ✅ / broken ❌]
GitHub backup:        [last push: X ago]
WhatsApp:             [connected ✅ / disconnected ❌]

━━━ MEMORY HEALTH ━━━
Daily notes:     [today's file exists? ✅/❌]
Long-term:       [MEMORY.md size — OK / bloated]
Learnings:       [count this week]
Last backup:     [X ago]

━━━ RECOMMENDATIONS ━━━
1. [Most important thing to fix]
2. [Second priority]
3. [Optional improvement]
```

---

## Running the Eval

### Step 1 — Self Performance Score

Score each dimension 1–5 based on today's activity:

```
Execution (1–5):
- 5: All tasks completed without reminders
- 3: Most tasks done, some follow-up needed
- 1: Multiple tasks missed or forgotten

Accuracy (1–5):
- 5: No corrections from owner
- 3: 1–2 corrections
- 1: Multiple errors or wrong outputs

Memory (1–5):
- 5: Recalled context correctly every time
- 3: Missed some context, caught on
- 1: Repeated the same mistakes

Proactivity (1–5):
- 5: Acted before being asked multiple times
- 3: Responded to requests, minimal initiative
- 1: Only reacted, no proactive actions

Communication (1–5):
- 5: Clear, concise, no unnecessary narration
- 3: Occasionally verbose or unclear
- 1: Shared reasoning, listed options, narrated steps
```

### Step 2 — Task Audit

```bash
TASKS_FILE="$HOME/.openclaw/workspace/memory/tasks.md"

echo "Tasks done:"
grep -c "\[x\]" "$TASKS_FILE" 2>/dev/null || echo 0

echo "Tasks in progress:"
grep -c "\[ \]" "$TASKS_FILE" 2>/dev/null || echo 0

# Stalled = in progress for 2+ days
echo "Stalled tasks (2+ days old):"
grep "\[ \]" "$TASKS_FILE" | grep -v "$(date +%Y-%m-%d)" | grep -v "$(date -u -d '1 day ago' +%Y-%m-%d 2>/dev/null)" || echo "none"
```

### Step 3 — PA Network Health

```bash
BILLING_FILE="$HOME/.openclaw/workspace/memory/billing-status.json"

echo "PA Network Status:"
python3 << 'PYEOF'
import json
data = json.load(open('/opt/ocana/openclaw/workspace/memory/billing-status.json'))
for pa in data['issues']:
    status = "✅" if pa['status'] == 'resolved' else "⚠️"
    print(f"  {status} {pa['pa']} ({pa['owner']}): {pa['status']}")
PYEOF
```

### Step 4 — Skills Audit

```bash
SKILLS_DIR="$HOME/.openclaw/workspace/skills"

echo "Installed skills:"
ls "$SKILLS_DIR" | grep -v README | wc -l

echo "Skills list:"
ls "$SKILLS_DIR" | grep -v README
```

### Step 5 — Integration Health

```bash
# Test Anthropic billing
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: ${ANTHROPIC_API_KEY:-none}" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/models 2>/dev/null)

# Interpret result
if [ "$API_STATUS" = "200" ]; then echo "Billing: ✅ OK"
elif [ "$API_STATUS" = "402" ]; then echo "Billing: ❌ OUT OF CREDITS"
elif [ "$API_STATUS" = "401" ]; then echo "Billing: ❌ Invalid key"
else echo "Billing: ? HTTP $API_STATUS"
fi

# Test GitHub backup
LAST_PUSH=$(git -C "$HOME/.openclaw/workspace" log -1 --format="%ar" 2>/dev/null)
echo "Last backup: $LAST_PUSH"

# Test monday.com
if [ -f "$HOME/.credentials/monday-api-token.txt" ]; then
  MONDAY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST https://api.monday.com/v2 \
    -H "Authorization: $(cat $HOME/.credentials/monday-api-token.txt)" \
    -H "Content-Type: application/json" \
    -d '{"query": "{ me { id } }"}' 2>/dev/null)
  [ "$MONDAY_STATUS" = "200" ] && echo "monday.com: ✅" || echo "monday.com: ❌ ($MONDAY_STATUS)"
else
  echo "monday.com: ? (no token found)"
fi
```

### Step 6 — Memory Health

```bash
TODAY=$(date -u +%Y-%m-%d)
WORKSPACE="$HOME/.openclaw/workspace"

# Check daily notes exist
[ -f "$WORKSPACE/memory/$TODAY.md" ] \
  && echo "Daily notes: ✅" \
  || echo "Daily notes: ❌ not created yet"

# Check MEMORY.md size (warn if >200 lines)
MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)
if [ "$MEMORY_LINES" -gt 200 ]; then
  echo "MEMORY.md: ⚠️ Large ($MEMORY_LINES lines) — consider pruning"
else
  echo "MEMORY.md: ✅ ($MEMORY_LINES lines)"
fi

# Count learnings this week
LEARNINGS=$(grep -c "^##" "$WORKSPACE/.learnings/LEARNINGS.md" 2>/dev/null || echo 0)
echo "Total learnings logged: $LEARNINGS"
```

---

## Recommendations Logic

After running all steps, generate recommendations:

```
If any PA has billing_error AND status != resolved:
  → "Fix billing for [PA list] — they can't function"

If any task has status in_progress for 2+ days:
  → "Follow up on stalled task: [task name]"

If MEMORY.md > 200 lines:
  → "Prune MEMORY.md — it's getting bloated"

If daily notes don't exist:
  → "Create today's memory file"

If last backup > 6 hours ago:
  → "Run git backup"

If API billing = 402:
  → "My own API key is out of credits — alert the admin immediately"
```

---

## Scheduling

Run eval:
- **On demand** — when owner asks
- **Weekly** — every Sunday at 09:00
- **After major incidents** — billing crisis, WA disconnect, etc.

---

## Cost Tips

- **Cheap**: Reading files, scoring, formatting — any small model
- **Expensive**: Summarizing large memory files — skip if not asked
- **Avoid**: Running all API health checks every hour — cache for 30 min
- **Batch**: Run all health checks in one pass, not one at a time

---

## Minimum Model

Any model that can:
1. Read files
2. Apply if/then scoring rules
3. Format a structured report

No advanced reasoning needed.

---

## PA Performance Scoring (Merged from pa-eval skill)

Use this section when evaluating individual PA agents (weekly self-eval or on-demand when owner gives feedback).

### Scoring Dimensions (1–5 each, max 40 points)

| Dimension | What to Measure |
|---|---|
| **Execution** | Tasks completed without reminders |
| **Accuracy** | Results are correct and complete |
| **Speed** | Response time is fast |
| **Proactivity** | Acts without being asked |
| **Communication** | Concise and context-appropriate |
| **Memory** | Remembers context across sessions |
| **Tool Use** | Tools used correctly and efficiently |
| **Judgment** | Knows when to act vs. when to ask |

**Grade:** A (36–40), B (28–35), C (20–27), D (<20)

### Owner Feedback Signals

Log these automatically when detected:

| Signal | Action |
|---|---|
| 👍 reaction / "thanks" / "great" | Log +1 positive |
| 👎 reaction / "wrong" / "not good" | Log -1, record the correction |
| Owner re-asks the same question | Log -1 memory gap |
| Owner does the task themselves | Log -1 initiative gap |
| Owner surprised by proactive action | Log +2 proactivity |

**Rule:** Log feedback signals immediately — don't batch them.

### Weekly Eval File

Save to `.learnings/eval/YYYY-MM-DD.md` with: scores table, owner feedback, tasks completed/failed, what went well, what to improve, actions for next week.

### Benchmark Tests (Run Monthly)

- **Task Completion Rate:** `completed / assigned × 100%` — Target: >90%
- **Accuracy Rate:** `(tasks - corrections) / tasks × 100%` — Target: >95%
- **Memory Retention:** Ask about something discussed 7+ days ago — Target: >80% recall
