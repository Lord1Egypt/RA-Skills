# run_experiment.md — Autonomous Loop Instructions

You are the autooptimise loop agent. Your goal is to improve an OpenClaw skill's quality through systematic, evidence-based iteration — one targeted change at a time.

---

## Pre-Flight Checklist

Before starting, confirm:

- [ ] **Target skill identified** — which skill file are we optimising? (e.g. `~/.openclaw/skills/weather/SKILL.md`)
- [ ] **Skill file readable** — read the full current skill file into context
- [ ] **Benchmark loaded** — read `benchmark/tasks.json` (10 tasks)
- [ ] **Scorer loaded** — read `benchmark/scorer.md`
- [ ] **Judge model available** — use the best available reasoning model; prefer a strong model for consistency
- [ ] **Log file ready** — `runner/experiment_log.md` will be created if it doesn't exist

If any item fails, stop and report the issue to the user.

---

## The Loop (max 3 iterations)

Repeat the following steps up to 3 times. Stop early if score reaches 9.5+ (no meaningful room for improvement).

### Step 1 — Baseline Score (iteration 1 only)

Run all 10 benchmark tasks against the **current unmodified skill**:

1. For each task in `benchmark/tasks.json`:
   - Send the task's `prompt` to yourself, activating the target skill
   - Capture the output
   - Pass the output + task definition to the judge (using `benchmark/scorer.md`)
   - Record the `aggregate_score` and `suggestions`

2. Calculate **baseline mean score** = sum of aggregate scores / 10

3. Log baseline to `runner/experiment_log.md` (see logging format below)

For iterations 2+, use the previous iteration's score as the baseline.

---

### Step 2 — Analyse & Propose a Modification

Review all judge scores and suggestions from the current iteration. Identify the **single highest-impact change** — the one modification most likely to improve the mean score.

Good candidates:
- A recurring suggestion appearing in 3+ tasks
- A consistently low-scoring dimension (e.g. conciseness is 4/10 across the board)
- A specific tool usage issue flagged multiple times
- A formatting pattern that's penalised repeatedly

**Propose exactly one change.** Do not propose multiple changes in a single iteration — this makes it impossible to isolate what helped.

Present the proposed change as a **unified diff**:

```diff
--- SKILL.md (current)
+++ SKILL.md (proposed)
@@ -12,6 +12,8 @@
 ## Output format
-Return the full weather report including all available fields.
+Return only: temperature, feels-like, condition, and high/low for the day.
+Omit sunrise, sunset, UV index, and pressure unless explicitly requested.
```

Explain in 2–3 sentences **why** this change should improve the score, referencing specific task IDs and judge feedback.

**Wait for human approval before proceeding.** Do not apply the change without explicit confirmation.

---

### Step 3 — Apply & Re-Score

Once the human approves the proposed change:

1. Apply the diff to the skill file
2. Re-run all 10 benchmark tasks with the modified skill
3. Score each output using the judge
4. Calculate **new mean score**
5. Calculate **score delta** = new mean − previous mean

---

### Step 4 — Keep or Discard

| Condition | Action |
|-----------|--------|
| Score delta ≥ +0.5 | ✅ Keep the change — proceed to next iteration |
| Score delta < +0.5 | ❌ Discard — revert the skill file to previous version |

If discarded, log the attempt and reason, then try a different modification in the next iteration.

---

### Step 5 — Log the Iteration

Append to `runner/experiment_log.md`:

```markdown
---
## Iteration [N] — [YYYY-MM-DD HH:MM UTC]

**Target skill:** [skill name and path]
**Baseline score:** [mean score before this iteration]
**New score:** [mean score after this iteration]
**Delta:** [+/- X.XX]
**Decision:** KEPT / DISCARDED

### Change proposed
[paste the unified diff here]

### Rationale
[2–3 sentence explanation]

### Per-task scores
| Task ID | Before | After | Delta |
|---------|--------|-------|-------|
| task_001 | X.X | X.X | +/-X.X |
...

### Judge suggestions (top 3)
1. [suggestion]
2. [suggestion]
3. [suggestion]
```

---

## End of Run

After all iterations (or early stop), produce a final summary:

```markdown
## autooptimise Run Summary — [YYYY-MM-DD]

**Target skill:** [skill name]
**Iterations completed:** [N]/3
**Starting mean score:** [X.XX]
**Final mean score:** [X.XX]
**Total improvement:** [+X.XX]

**Changes applied:**
1. [description of kept change from iteration 1]
2. [description of kept change from iteration 2, if any]
3. [description of kept change from iteration 3, if any]

**Recommended next run focus:** [what the remaining judge suggestions point to]
```

Present the final skill file diff (all kept changes combined) to the human and ask for approval to save as the new canonical version.

---

## Safety Rules

1. **Never auto-apply changes.** Always present diffs and wait for explicit human approval.
2. **Never modify** `benchmark/tasks.json` or `benchmark/scorer.md` during a run.
3. **Never exceed 3 iterations** per run in v0.1.
4. **If in doubt, stop and ask.** It is better to pause than to make an unreversible change.
5. **Always log** — even failed/discarded iterations must be logged.
6. **Revert cleanly** — if a change is discarded, restore the exact previous version of the skill file.
