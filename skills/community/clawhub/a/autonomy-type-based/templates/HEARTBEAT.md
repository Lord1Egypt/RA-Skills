# Type-Based Autonomy Heartbeat

**Follow this protocol to work autonomously on specific task types.**

---

## Step 0: Check Context & Checkpoint (MANDATORY FIRST)

- [ ] Check context % right now: _____%
- [ ] If ≥ 70%: Attempt checkpoint (non-blocking)
  - Write to `memory/YYYY-MM-DD.md` using write tool
  - Format: See `references/checkpoints.md` (included in this skill)
  - If write fails (file error/unable): Log warning, continue anyway
  - **Do NOT block** on checkpoint failures
- [ ] If checkpoint written or failed gracefully: Continue to Step 1

**Checkpoint fallback (if references/checkpoints.md not available):**
```markdown
## Checkpoint [HH:MM] — Context: XX%

**Current task:** [what we're working on]
**Status:** [progress summary]
**Resume:** [next step if context lost]
```

```

---

## Step 1: Check for URGENT items (30 seconds)

**Stop and handle immediately if:**
- Direct messages from RA waiting
- Critical blockers needing attention
- System health issues or errors
- Tasks with `@priority:urgent` (override everything)

**If urgent found:** Handle it first. Then skip to Step 5 (log and exit).
**If no urgent:** Continue to Step 2.

---

## Step 2: Check Current Mode

Read current state:

```
# Check if autonomy should work:

1. Are we in active session? (RA is actively messaging?)
   - YES: Skip autonomy, let RA direct work
   - NO: Continue to Step 3

2. Token budget check:
   - Tokens remaining < 5K for day?
     - YES: Skip autonomy, reply HEARTBEAT_OK
     - NO: Continue to Step 3
```

**If should NOT work:** Reply `HEARTBEAT_OK` and exit.

---

## Step 3: Pull from Type-Based Task Queue

**Read:** `tasks/QUEUE.md`

**Filter by task types:**
```markdown
ONLY work on these types:
- ✅ @type:research
- ✅ @type:writing
- ✅ @type:analysis

SKIP these types (cron handles):
- ❌ @type:maintenance
- ❌ @type:backup
- ❌ @type:security
```

**Selection logic:**
```
1. Read all tasks in "🔴 Ready" section
2. Filter for allowed types: research, writing, analysis
3. Sort by priority: urgent → high → medium → low
4. Pick the first task you can work on
5. If no matching tasks: Reply "HEARTBEAT_OK" and exit
```

---

## Step 4: Do the Work

**Move task to "🟡 In Progress":**
```markdown
## 🟡 In Progress
- [ ] @agent: @type:research @priority:high [Task description]
  - Started: 2026-02-16 HH:MM UTC
  - Progress: Working on it
```

**Work on task until:**
- Complete → Go to Step 4a
- Blocked → Go to Step 4b
- Time limit reached (~10-15 min) → Go to Step 4c
- Token budget near limit → Go to Step 4c

### 4a: Task Complete

**Move to "✅ Done Today":**
```markdown
## ✅ Done Today
- [x] @agent: @type:research @priority:high [Task description]
  - Completed: 2026-02-16 HH:MM UTC
  - Tokens used: ~XK
  - Output: [path to output file]
```

**If work spawns follow-up tasks, add to "💡 Ideas":**
```markdown
## 💡 Ideas
- [Idea: @type:analysis @priority:medium Analyze research findings for X]
```

### 4b: Task Blocked

**Keep in "🟡 In Progress" with blocker notes:**
```markdown
## 🟡 In Progress
- [ ] @agent: @type:writing @priority:high [Task]
  - Started: 2026-02-16 HH:MM UTC
  - BLOCKED: [What's blocking]
  - Needs: [What's needed to unblock]
```

### 4c: Time/Token Limited

**Keep in "🟡 In Progress" with progress notes:**
```markdown
## 🟡 In Progress
- [ ] @agent: @type:research @priority:high [Task]
  - Started: 2026-02-16 14:00 UTC
  - Progress: [What completed]
  - Resume: Next heartbeat session
```

---

## Step 5: Log and Report

**Log to `memory/[today].md`:**
```markdown
## Work Session

- Task: [Task description]
- Type: research/writing/analysis
- Priority: high/medium/low
- Started: HH:MM UTC
- Completed: HH:MM UTC (or IN PROGRESS)
- Tokens used: ~XK
- Output: [path] (or "N/A")
- Status: Complete / Blocked / In Progress

---

## Follow-up Tasks (from queue Ideas)

[Add any follow-up tasks that need to be promoted to Ready]
```

**If valuable finding or completion:**
- Check GOALS.md - does this advance RA's goal (MONEY)?
- Update GOALS.md with progress if relevant
- Add to `.learnings/` if it's an insight or lesson

---

## Step 6: Next Heartbeat Decision

**After current session:**

```
# Before replying:

- Task complete and time remaining?
  → Pick another allowed-type task if queue has one

- Task blocked?
  → Skip autonomy this session, reply HEARTBEAT_OK (wait for resolution)

- Token budget running low (< 5K remaining)?
  → Skip autonomy, reply HEARTBEAT_OK

- RA is actively messaging?
  → Skip autonomy, let RA direct work

 Otherwise:
  → Reply HEARTBEAT_OK
```

---

## Reminders

- **Work ONLY on:** `@type:research`, `@type:writing`, `@type:analysis`
- **SKIP:** `@type:maintenance`, `@type:backup`, `@type:security` (cron handles)
- **Priority order:** `urgent` → `high` → `medium` → `low`
- **Queue location:** `tasks/QUEUE.md`
- **Token budget:** ~12-32K/day (4 sessions × 3-8K each)

---

## When to Reply HEARTBEAT_OK

```
Any of these = HEARTBEAT_OK:
- RA is actively messaging (in conversation)
- Tokens remaining < 5K for day
- No matching tasks in queue (no research/writing/analysis ready)
- Just completed work and no more tasks remaining
- Task blocked and waiting for resolution
```

---

**Remember:** TYPE-BASED autonomy means filtering by task type, not time. Work whenever available, but ONLY on value-add tasks.
