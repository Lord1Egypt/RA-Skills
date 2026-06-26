---
name: daily-reflection
description: Nightly OpenClaw reflection routine for isolated cron jobs. Analyzes the day, extracts concrete learnings, updates solution memory, detects recurring patterns, and writes a morning briefing. Use for automated end-of-day memory consolidation, not routine chat replies.
---

# Daily Reflection Skill

Run this reflection fully. No step may be skipped.
All outputs are written to memory — not output as chat messages.

---

## STEP 1 — Day Analysis

Load all today's entries from memory (memory_search for "today", current date, active projects).

Answer these questions:

### Tasks
- Which tasks were completed today?
- Which were started but not finished?
- Why were unfinished tasks not completed?

### Bugs & Issues
- Which bugs were reported today?
- Which were solved — how?
- Which are still open?
- Which first fix attempts failed — why?

### Quality
- Were there any regressions today?
- Did I have to revert anything?

### Communication
- What did the user rate positively today?
- What did the user correct or reject?
- Were there misunderstandings?

---

## STEP 2 — Extract Learnings

Maximum 5 concrete learnings. Format:

```
LEARNING:
Situation: [What happened]
Error/Insight: [What was wrong or newly learned]
Better tomorrow: [Concrete behavior change]
Context-Tags: [e.g. NestJS, Auth, Backend, Debugging]
Priority: high / medium / low
```

---

## STEP 3 — Update Solution Memory

For each non-trivial bug solved today:

```json
{
  "id": "[timestamp]-[short-name]",
  "problem": "[Problem in one sentence]",
  "symptoms": ["[Symptom 1]", "[Symptom 2]"],
  "root_cause": "[The actual cause]",
  "solution": "[What was concretely changed]",
  "code_snippet": "[Optional: key code fix]",
  "context_tags": ["Tag1", "Tag2"],
  "project": "[Project name]",
  "confidence": 0.95,
  "solved_at": "[Date]",
  "time_to_solve_minutes": 0
}
```

Write to memory under `solution_memory/[id].json`.

---

## STEP 4 — Pattern Detection (last 7 days)

Check memory_search over last 7 days:
- Are there recurring errors?
- Are there task types where time is consistently underestimated?
- Are there areas where bugs cluster?

Format:
```
PATTERN DETECTED:
Observation: [What repeats]
Frequency: [X times in Y days]
Countermeasure: [Concrete future behavior or rule to propose]
```

---

## STEP 5 — Write Morning Briefing

Write to `memory/morning-briefing.md` (overwrite) AND archive as `memory/briefings/[tomorrow-date].md`:

```
🌅 MORNING BRIEFING — [Tomorrow's date]

📋 OPEN TASKS (Priority):
1. [Task] — [why important today]
2. [Task]
3. [Task]

🔴 OPEN BUGS:
- [Bug] — [last status]

💡 TODAY'S LEARNINGS (top 3):
- [Learning 1]
- [Learning 2]
- [Learning 3]

⚠️ WATCH OUT TOMORROW:
- [What to pay special attention to]

🎯 FOCUS TOMORROW:
[One sentence on what's most important]
```

**After writing:** archive a copy under `memory/briefings/[tomorrow-date].md` using normal file-write tools. Do not run shell commands unless the host policy allows it.

---

## STEP 6 — Write Daily Memory

Write structured summary to `memory/YYYY-MM-DD.md` (append).

Format:
```
## 23:59 Reflection

### Completed today
- [Task 1]
- [Task 2]

### Open / In Progress
- [Task]

### What went well
- [Concrete things that worked — code, communication, decisions]

### What went poorly
- [Honest — errors, misunderstandings, bad decisions]

### Learnings
- Situation: [What happened] → Better tomorrow: [Concrete change]

### New Patterns
- If new pattern detected → write to memory/patterns.md
- If no new pattern: "No new patterns"

### Solution Memory Updates
- [ID] — [short description]
```

**REQUIRED:** What went well + What went poorly + Learnings must ALWAYS be filled in.

---

## STEP 7 — Memory Cleanup

- Mark temporary debug entries from today as stale when clearly obsolete
- Mark outdated patterns; do not delete uncertain information without review

## STEP 8 — Session Quality Score

Rate today's session objectively (0-10):

```
📊 SESSION QUALITY — [Date]
Helpful: [0-10] — Did the user get what they needed?
Response time: [0-10] — Was I fast and direct?
Errors: [0-10] — How many corrections? (10 = none)
Proactivity: [0-10] — Did I anticipate problems?
Total: [Average]

What lowered quality today: [specific]
What raised it: [specific]
```

Write to `memory/session-quality-log.md` (append).
If Total < 7 → analyze main reason and propose a new pattern for review.

## STEP 9 — Evaluate Cron Prompts

Check last outputs of key crons (read archived briefings):
- Were they relevant? Too long? Too short?
- If a prompt produced poor results → propose a concrete improvement; only update cron jobs after explicit user approval

---

## OUTPUT RULE

Keep user-facing output minimal. Prefer memory files for routine results.

Exception: if a critical open problem cannot wait, send one short message:
`⚠️ Reflection done — critical issue: [1 sentence]`

---

## SOLUTION MEMORY — CONSULT BEFORE DEBUGGING

**BEFORE any debugging attempt:**
1. `memory_search("solution_memory [keywords from bug description]")`
2. Relevant solutions found → try these first
3. No solutions → debug normally, then write to solution memory

**BEFORE similar tasks:**
1. `memory_search("solution_memory [task-type]")`
2. Similar past tasks → use time estimate and known pitfalls
