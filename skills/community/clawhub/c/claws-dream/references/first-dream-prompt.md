# First Dream — Initial Memory Setup

Run immediately after installing the skill. Do NOT wait for the cron schedule.

## Goal

Scan existing daily logs, initialize memory architecture, and send a before/after report.

---

## Step 1: Initialize Directory Structure

```bash
mkdir -p memory/episodes
```

Ensure these files exist (create from templates if missing):
- `memory/index.json`
- `memory/procedures.md`
- `memory/dream-log.md`
- `memory/archive.md`

## Step 2: Snapshot BEFORE

Count current state:
```
MEMORY_LINES = wc -l MEMORY.md (0 if doesn't exist)
SECTIONS = count non-empty section headers in MEMORY.md
```

## Step 3: Scan Existing Daily Logs

If `memory/YYYY-MM-DD.md` files exist:
- Read all of them
- Extract: decisions, facts, preferences, lessons, todos
- Categorize into MEMORY.md sections

If no daily logs exist:
- Create initial MEMORY.md structure from template
- Create empty index.json

## Step 4: Build index.json

For each new memory entry, create:
```json
{
  "id": "mem_001",
  "summary": "One-line summary",
  "source": "memory/YYYY-MM-DD.md",
  "target": "MEMORY.md#section-name",
  "created": "YYYY-MM-DD",
  "lastReferenced": "YYYY-MM-DD",
  "referenceCount": 1,
  "importance": 0.5,
  "tags": [],
  "related": [],
  "archived": false
}
```

## Step 5: Generate First Report

Append to memory/dream-log.md:

```markdown
## 🌟 First Dream — YYYY-MM-DD

**Initialized memory architecture from scratch**

📊 Before: 0 entries, 0 sections
📊 After: {N} entries, {M} sections

🧠 Memory Health: {score}/100
   • Freshness: {X}%
   • Coverage: {X}%
   • Coherence: {X}%
   • Efficiency: {X}%
   • Reachability: {X}%

📝 Initialized sections:
   • Core Identity
   • User
   • Projects
   • Business
   • People & Team
   • Strategy
   • Key Decisions
   • Lessons Learned
   • Environment
   • Open Threads

🎉 Your memory system is ready!
```

## Step 6: Send Notification

```
🌟 First Dream complete!

🧠 Memory initialized: {N} entries across {M} sections
📊 Health Score: {score}/100

Your memory architecture is ready. Every night, I'll consolidate new information and keep your memory fresh.

💬 Let me know if you'd like to adjust any memories
```

Then END.
