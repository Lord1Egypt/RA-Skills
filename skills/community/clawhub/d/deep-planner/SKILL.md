---
name: deep-planner
description: |
  A meta-skill that activates before complex tasks to enforce structured planning,
  step-by-step execution, and self-reflection. Works like Claude Code's TodoList —
  generates a visible task plan, persists it to `.todolist/`, checks off steps as
  they complete, and pauses at critical decision points for user confirmation.

  Trigger this skill whenever:
  - The request involves 3+ steps or multiple tools/skills chained together
  - Keywords like "research", "analyze", "plan", "design", "compare", "write a report" appear
  - Key variables are undefined (audience, platform, format, scope, constraints)
  - The domain is unfamiliar or information may be time-sensitive
  - A task requires coordinating more than one other skill

  This skill does NOT produce the final output — it plans and supervises execution,
  then delegates to the appropriate domain skills (e.g. web search, code execution,
  platform-specific skills). Think of it as the project manager, not the worker.
---

# Deep Planner

A planning, execution, and self-reflection protocol for complex agent tasks.

## How It Works

The TodoList exists in two places simultaneously:
- **In the reply** — visible to the user, updated as steps complete
- **In `.todolist/`** — persisted to disk, recoverable if context is truncated

Both stay in sync. The file is the backup; the conversation is the live view.

---

## Execution Protocol

### Step 0 — Resume or Start Fresh

Before anything else, check for interrupted tasks:

```
Scan .todolist/ for any file with status: in-progress
  Found → Read it, show the user the current state, ask: continue or start new?
  Not found → Proceed to Step 1
```

---

### Step 1 — Parse the Request (internal, not shown to user)

Before generating a plan, resolve the following internally:

```
□ What is the core goal? (one sentence)
□ What is the final deliverable? (report / code / content / action sequence / ...)
□ What tools or skills are needed? (web search / browser / code execution / ...)
□ Are there any ambiguities that would lead to completely different execution paths?
    Yes → Ask the user first, then generate the TodoList
    No  → Make reasonable assumptions; document them in the plan's Assumptions block
```

**Only stop to ask about blockers — not details you can reasonably infer.**
Consolidate all questions into a single message. Do not ask one at a time.

---

### Step 2 — Generate the TodoList

Once the request is clear, output the plan and write it to disk simultaneously.

**Format shown in the reply:**

```markdown
## 📋 Task Plan: {short task name}

**Goal:** {one-line description of the final deliverable}
**Steps:** {N}

---

- [ ] 1. {step description} `{tool or skill}`
- [ ] 2. {step description} `{tool or skill}`
- [ ] 3. {step description} `internal reasoning`
- [ ] ...

> 💡 Assumptions: {any assumptions made without user confirmation}

---
Starting step 1 →
```

**Write to disk** at `.todolist/YYYYMMDD-{task-name}.md` using the file format below.

---

### Step 3 — Execute Step by Step

Work through the TodoList in order. After each step completes:

1. Open the next reply with a status update — mark the step `[x]`
2. Briefly describe what was produced (1–2 sentences)
3. Update the file to reflect the new state
4. Proceed to the next step

**Reply header format (concise):**
```
✅ Step 2 done → Starting step 3...
```

**Pause and ask the user when:**
- A step is marked ❓ (critical information is missing)
- Reality diverges significantly from the plan and replanning is needed
- A tool call fails and there are multiple recovery paths to choose from

---

### Step 4 — Wrap Up

When all steps are done:

1. Show the fully checked-off TodoList in the reply
2. Run the post-completion reflection check (see below)
3. Update the file: set `status: completed` — leave the file in place, do not delete

---

## Confidence Levels

Only annotate when uncertain. Do not label every step.

| Mark | Meaning | Action |
|------|---------|--------|
| (default) | Confident, proceed | Execute directly |
| ⚠️ | May involve inference or outdated info | Execute, flag uncertainty in output |
| ❓ | Critical info missing | Pause, ask the user, then continue |

---

## Post-Completion Reflection

Run internally after all steps finish. **Only surface issues that actually exist.**

```
□ Was the core goal achieved?
□ Did I state anything I believed but didn't verify?  → Flag it
□ Are there ⚠️ steps whose conclusions need a caveat?
□ Is the deliverable complete with nothing skipped?
```

If issues exist, append to the final reply:
```
> ⚠️ Note: {X} is based on inference — consider verifying {specific thing}.
```

---

## Anti-Hallucination Rules

These constraints are non-negotiable:

1. **No fabricated data** — statistics, market figures, and research findings must have a source, or be explicitly labeled as estimates
2. **No fabricated citations** — do not reference papers, reports, or news articles that may not exist
3. **Flag time-sensitive claims** — anything described as "latest", "current", or "now" must note the knowledge cutoff date or recommend the user verify with a live search
4. **Be honest about limits** — if a task is out of scope, say so clearly rather than producing low-confidence output

---

## File Format

Path: `.todolist/YYYYMMDD-{task-name}.md`

```markdown
# {Task Name}
Created: YYYY-MM-DD HH:MM
Status: in-progress | completed

## Goal
{One-line description of the final deliverable}

## TodoList
- [x] 1. {completed step}
- [x] 2. {completed step}
- [ ] 3. {current step} ← current
- [ ] 4. {upcoming step}

## Assumptions & Confirmations
- Assumed: {things inferred without user confirmation}
- Confirmed: {things the user explicitly answered}

## Progress
{done}/{total} steps completed
```

---

## Task Type Templates

For common task types, load the matching template from the reference file:

| Task Type | Reference |
|-----------|-----------|
| Research & analysis | `references/task-types.md#research` |
| Content creation (articles, posts) | `references/task-types.md#content` |
| Technical design | `references/task-types.md#technical` |
| Data processing | `references/task-types.md#data` |
| Multi-skill pipelines | `references/task-types.md#multi-skill` |

---

## Skill Coordination

This is a **meta-skill**. It plans and monitors; domain skills do the work.

```
User request
  → [deep-planner] parse + plan + write TodoList to disk
      → [web search / browser] information gathering steps
      → [domain skill A] content or processing steps
      → [domain skill B] platform-specific steps
  → [deep-planner] reflection + mark file as completed
```

Do not perform content generation, file operations, or network requests inside this skill. Delegate those to the appropriate tools and skills.
