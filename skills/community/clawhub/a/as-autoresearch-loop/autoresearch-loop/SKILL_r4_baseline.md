---
name: autoresearch-loop
description: >
  Apply Karpathy's autoresearch methodology to autonomously iterate and improve anything measurable —
  Claude skills, n8n workflows, system prompts, business processes, or any artifact with a clear quality metric.
  Inspired by github.com/karpathy/autoresearch (56k stars). The loop: propose a change → test it → measure
  against the target metric → keep if better, discard if not → repeat indefinitely.

  ALWAYS trigger this skill when the user says things like: "improve this skill automatically", "iterate on this
  workflow", "run autoresearch on", "autonomous improvement loop", "overnight experiments", "keep iterating until
  it's better", "run experiments on this", "optimize this automatically", or any request to have Claude
  autonomously make and test changes to something measurable. Also trigger for requests to "set up an improvement
  loop", "run the autoresearch method", or anything involving iterative autonomous experimentation.
---

# Autoresearch Loop Skill

Karpathy's autoresearch methodology applied to improving Claude skills, n8n workflows, system prompts, and business processes.

**Core idea**: Define what "better" means. Lock everything except the artifact being improved. Propose a change → test → measure → keep or discard → repeat. Never stop until interrupted.

**When NOT to use this loop:**
- You can't define a single measurable metric (e.g. "improve my writing style" — too subjective)
- The artifact is too large to evaluate cheaply in a fixed budget
- There's no fixed eval set (or you can't create one) — without a stable yardstick, you're just guessing
- You need to improve two interdependent artifacts simultaneously — do them sequentially instead

If you can't answer "what number tells me if this experiment worked?", stop and define that first.

---

## Setup Phase

Before the loop starts, establish these five things with the user:

### 1. The Artifact (What You're Improving)
The single file, document, workflow, or process being iteratively modified. Think of this as `train.py` in Karpathy's repo — the one thing the agent edits.

Examples:
- A `SKILL.md` file
- An n8n workflow JSON
- A system prompt
- An SOP document
- A business process description

**Fixed files**: Identify what must NOT change — the evaluation criteria, input test cases, external integrations. These are your `prepare.py`.

### 2. The Metric (What "Better" Means)
One clear, measurable signal that determines keep vs. discard. Lower or higher must unambiguously mean better.

Examples by artifact type:

| Artifact | Good Metric |
|---|---|
| Claude skill | Pass rate on test prompts (0–100%) |
| System prompt | Accuracy score on eval set |
| n8n workflow | Successful execution rate, latency, step count |
| Business process | Cycle time, error rate, steps to completion |
| SOW template | Readability score, required fields coverage |

**If you can't define a metric, you can't run the loop.** Work with the user until there's one.

**Building a composite metric** — if you care about two dimensions (e.g., accuracy AND conciseness):
1. Score each dimension separately on the same eval set (e.g., accuracy: 0–1 per prompt, conciseness: 0–1 per prompt)
2. Define weights based on relative importance *before the loop starts*: `score = 0.7 * accuracy + 0.3 * conciseness`
3. The composite score is what goes in results.tsv — one number, decisive
4. Never adjust the weights mid-loop based on results — that's changing the metric, which invalidates comparisons
5. Document the weights in results.tsv header or a separate note so future sessions know what they're comparing against

### 3. The Budget (Experiment Scope)
What one experiment consists of. Keep it short — Karpathy uses 5 minutes per training run. Translate to your domain:

- Skill: run N test prompts through Claude (N = 5–20; use a fast subset for iteration, the full set before committing a keep on borderline results)
- Workflow: execute on M sample inputs
- Process: dry-run or peer review against checklist

**What makes a good eval set:**
- **Diverse** — covers all the main use cases of the artifact, not just the happy path
- **Adversarial** — includes inputs that should fail gracefully, edge cases, ambiguous inputs
- **Stable** — prompts that have clear, unambiguous pass/fail criteria; avoid prompts where "it depends"
- **Representative** — if the artifact handles 5 different scenarios, have prompts for each

A bad eval set (10 nearly identical prompts) will give you a misleadingly high score. If you improve from 60% to 80% but all 8 passing prompts are the same scenario, you've learned nothing about the other scenarios.

**Building an eval set from scratch** — if none exists:
1. List every distinct use case and scenario the artifact is supposed to handle
2. For each scenario, write 1–2 prompts: one normal case, one edge/adversarial case
3. Aim for 10–20 prompts total — enough for meaningful signal, small enough to run fast
4. Write the pass/fail criteria for each prompt BEFORE running any experiments — don't define "pass" after seeing the output
5. If you have real historical inputs (e.g., past emails, past requests), use those as the foundation — they're more realistic than synthetic ones

Do not start the loop until the eval set is complete and criteria are written.

### 4. The Results Log
Create `results.tsv` (tab-separated) with these columns:

```
iteration	score	status	description
```

- `iteration`: sequential number
- `score`: the metric value (numeric)
- `status`: `keep`, `discard`, or `error`
- `description`: what this experiment tried (keep under 100 chars)

Example:
```
iteration	score	status	description
0	62.5	keep	baseline
1	75.0	keep	added explicit output format section
2	68.0	discard	removed examples — hurt performance
3	80.0	keep	added failure mode handling + retry guidance
```

### 5. Confirm and Go
Show the user the setup summary:
- Artifact: [path/name]
- Metric: [what you're measuring and direction]
- Budget: [what one experiment costs]
- Baseline: will be measured on first run

Get confirmation, then kick off the loop.

---

## The Experiment Loop

**LOOP FOREVER** (until the user manually interrupts):

```
LOOP:
  1. READ current artifact + results log
  2. PROPOSE one targeted change (hypothesis-driven)
  3. APPLY the change to the artifact
  4. RUN the evaluation (execute test budget)
  5. MEASURE the metric
  6. DECIDE: keep or discard
  7. LOG to results.tsv
  8. REPEAT
```

### Step 2: Proposing a Change

Each experiment tests **one hypothesis**. A good hypothesis has three parts:
1. **What** you're changing (specific, not vague)
2. **What** you predict will happen (which prompts will now pass)
3. **Why** you expect that mechanism to work

❌ Bad: "change something" / "add more examples"
✅ Good: "If I add 3 concrete examples showing edge-case handling, adversarial prompts will start passing because the model currently lacks pattern context for those cases."

**Experiment prioritization** — run in this order for fastest signal:
1. Fix failures identified in the last eval run (highest signal, already know what broke)
2. Simplifications — remove something and retest (free wins, low risk)
3. Targeted additions for specific failing prompts
4. Structural restructuring
5. Radical rewrites (last resort after incremental plateau)

**Escalation rule**: If 8+ consecutive experiments discard on incremental changes, escalate to a radical rewrite of the artifact. One big structural change is still one experiment. If it discards, your backup brings you right back.

**Simplicity criterion (from Karpathy)**: All else equal, simpler is better.
- A 2% improvement with 30 new lines: probably not worth it
- A 2% improvement by deleting 10 lines: definitely keep
- 0% change but much cleaner: keep the simpler version

### Step 4: Running the Evaluation

**Handling noisy metrics**: LLM-based evaluations are non-deterministic — the same artifact can score 74% one run and 81% the next. Strategies:
- **Multi-run averaging**: Run the eval 3 times, take the mean. Require improvement > the noise floor (e.g., +5%) before keeping.
- **Noise floor rule**: If your runs vary by ±7%, a +3% improvement is meaningless — it's within noise. Only keep changes that beat the noise floor.
- **Deterministic scoring**: Use pass/fail rubrics with binary criteria where possible — they're less noisy than 1–5 scales.

If your eval is highly noisy, averaging 3 runs before deciding keep/discard is the minimum. Treat single-run scores with suspicion.

**For Claude Skills:**
Take the test prompts provided (or generate them). For each prompt:
1. Load the skill SKILL.md into context
2. Follow the skill to complete the task
3. Score against the rubric (pass/fail or 0–100)
4. Average across all prompts = the metric

**For n8n Workflows:**
Run against sample inputs (or simulate execution):
1. Trace through the workflow node by node
2. Check for: correct output, no dead paths, expression validity
3. Count successes / total runs

**For System Prompts:**
Run a fixed set of adversarial + normal prompts:
1. Does it follow instructions correctly?
2. Does it handle edge cases?
3. Score each on a 1–5 rubric, average

**For Business Processes / SOPs:**
Evaluate against a checklist of requirements:
1. Coverage: does it address all required scenarios?
2. Clarity: could a new person follow it?
3. Completeness: no missing steps?
Score = % of checklist items passed

### Step 6: Keep or Discard

| Condition | Action |
|---|---|
| Score strictly improved | **KEEP** — advance to next iteration from this version |
| Score equal or worse | **DISCARD** — revert artifact to previous version |
| Evaluation errored | **ERROR** — log, investigate, fix or skip |

On discard: restore the artifact to its previous state before trying the next experiment.

**Regression risk**: The metric is only trustworthy if your eval set is well-designed. If you notice the artifact seems worse at something NOT in your eval set (e.g., it now handles Spanish inputs poorly), treat that as a red flag. You have two options: discard the change on principle, or note the gap and add a Spanish-language prompt to the NEXT session's eval set. The metric is king — but only if it measures the right things.

**Metric gaming / Goodhart's Law**: "When a measure becomes a target, it ceases to be a good measure." After 20–30 experiments, high scores (95%+) on a fixed eval set may reflect overfitting to those specific prompts rather than genuine improvement. Signs: score is high but real-world performance feels flat. Fix: redesign the eval set for the next session with harder, more diverse prompts. The loop is only as good as its yardstick.

### Step 7: Logging + Version Control

Always log before the next iteration starts.

**Backup pattern** — after every KEEP, save a versioned copy:
```bash
cp SKILL.md SKILL_v3.md   # or whatever iteration number
```

**Revert pattern** — on a DISCARD, restore before the next experiment:
```bash
cp SKILL_v3.md SKILL.md   # restore last kept version
```

Log the discard entry in results.tsv BEFORE reverting, so the history is complete.

If you're using git: `git stash` or `git checkout -- <file>` works just as well. The key is that you always have a clean last-known-good to return to.

---

## Rules

**EVAL IS IMMUTABLE**: Once the loop starts, the test set and scoring rubric cannot change. Adding, removing, or modifying eval prompts mid-loop invalidates all previous scores — you can no longer compare iterations fairly. If you discover a missing edge case, note it for the next session's eval set. Don't touch the current one.

**NO SCOPE CREEP**: The artifact's purpose cannot expand mid-loop. If you started improving a consulting SOW template and realize it should also cover retainer agreements, that's a scope change — not a content improvement. The existing eval set doesn't test the new scope, so any score change is meaningless. Finish the current loop for the original scope. Start a fresh loop with a new eval set for the expanded scope.

**BASELINE FIRST**: Iteration 0 is always a zero-change run. Do not modify the artifact. Run the evaluation as-is to establish the baseline score. Every future experiment is compared against this number. Without a clean baseline, you have nothing to beat.

**If the baseline looks broken** (e.g., 10% on a reasonable eval set): do NOT start experimenting from there. Investigate first — is the eval set miscalibrated? Is the artifact fundamentally broken before you started? Is the scoring rubric too strict? Fix the root cause (artifact or eval), then re-run the baseline as a clean iteration 0. Experimenting on top of a broken baseline wastes every experiment on debugging rather than improvement.

**NEVER STOP (mid-session)**: Once the loop starts, do not pause to ask the user if you should continue. The human might be away. Run until manually interrupted. If you run out of ideas, think harder — look at failed test cases, try the inverse of something that worked, try combining near-misses, escalate to a radical rewrite.

**Stopping for the day is fine**: "Never stop" means don't pause mid-session to ask permission. It does not mean you can never end a work session. When the human says they're done for the day: save the best artifact version, ensure results.tsv is up to date, note the top 2–3 experiment ideas to try next session. Resume tomorrow using the Resuming a Session guide. The loop continues across sessions — it doesn't reset.

**Principled stopping criteria**: "Never stop" applies mid-session, but a loop can legitimately run its course. Consider stopping when ALL of these are true: (1) score ≥ 95% on a well-designed, diverse eval set, AND (2) 10+ consecutive discards across incremental, structural, and radical experiments, AND (3) you've already tried combining near-misses. At that point the eval set — not the artifact — is likely the bottleneck. Redesign the eval and start a fresh session.

**The good-enough decision**: At high scores (90%+), apply a cost/benefit lens. If the remaining failing prompts cover rare edge cases that almost never appear in practice, 92% may be genuinely good enough to ship — don't optimize for the last 8% if it has no real-world impact. If the failing prompts cover common scenarios, keep going. The loop is a tool, not a religion.

**ONE CHANGE AT A TIME**: Never bundle two *untested* hypotheses in one experiment. You won't know which one caused the result.

**Exception — combining near-misses**: If change A was tested and discarded (0% improvement) AND change B was tested and discarded (0% improvement), you may combine them in one experiment. The logic: individually they had no effect, so combining them can't be blamed on bundling. If the combo works, you accept not knowing which part drove it — that's fine. If it discards, revert to best-so-far as usual.

**ONE METRIC**: Pick exactly one metric before the loop starts and never change it. Two metrics create unsolvable keep/discard decisions — if one improves and one degrades, you're stuck. If you care about multiple dimensions, define a single weighted composite score before starting, not mid-loop.

**ONE ARTIFACT**: The loop improves exactly one artifact per session. Two artifacts (e.g., a system prompt AND the workflow that calls it) means you can't isolate what caused a score change. Finish one loop, ship it, then start a fresh loop for the next artifact.

**Parallel loops are fine**: One artifact per loop, but you can run multiple loops simultaneously on *different* artifacts with separate eval sets and separate results.tsv files. The constraint is isolation within a loop, not globally.

**Same-artifact parallel branching**: Running two experiments from the same baseline and picking the winner is valid — *if* you fully discard the loser and continue from the winner only. What's not valid: merging both into one artifact ("take the best of both"). That's bundling two untested changes and you lose isolation. Pick one winner, discard the other entirely, continue.

**Circular evals**: You cannot use autoresearch to improve the eval set itself — the eval IS the fixed metric. You'd need a meta-metric to evaluate the eval, which is circular. Instead: redesign the eval offline using human judgment, then start a fresh loop with the new set.

**TRACK LINEAGE**: Each experiment builds on the best-so-far, not the original baseline. You are walking uphill.

**TIMEOUT/ERROR HANDLING**: If an evaluation errors or produces unusable results, log it as `error`, investigate once, fix if trivial, skip if not. Don't spend more than 2 attempts on a broken experiment before moving on.

**LOG EVERYTHING**: Even bad experiments. Especially bad experiments. The history is your research memory.

---

## Resuming a Session

When you come back to a loop after a break:

1. **Read results.tsv** — understand exactly where the loop left off: last iteration number, best score achieved, what was kept vs discarded
2. **Load the current best artifact** — NOT the baseline. Find the last `keep` entry in results.tsv and load the corresponding versioned file (e.g., `SKILL_v5.md`). That is your starting point.
3. **Do NOT re-run the baseline** — it's already logged. Wasting an experiment re-running it is a mistake.
4. **Continue the loop** — propose the next experiment from where you left off, incrementing the iteration counter

The results.tsv is your research memory. It tells you what was tried, what worked, and what didn't. Read it before every session, not just the first one.

---

## Applying to Specific Artifact Types

Quick reference for good experiment ideas by type:

**Claude Skills**: add concrete examples, add "when not to use" section, strengthen trigger language, add edge case handling, reorder sections for clarity, add quick-reference tables

**n8n Workflows**: simplify multi-step logic into fewer nodes, add error handling branches, fix expression syntax, improve routing conditions, add validation before expensive operations

**System Prompts**: tighten instruction specificity, add formatting constraints, add failure mode handling, add few-shot examples, remove contradictory instructions

**Business Processes / SOPs**: eliminate redundant steps, add decision trees for edge cases, add rollback/error procedures, clarify ownership of each step, add measurable completion criteria

---

## Output at the End of a Session

When the user interrupts or the session ends, produce a **Research Summary**:

```
## Autoresearch Session Summary

**Artifact**: [name]
**Total experiments**: N
**Starting score**: X
**Ending score**: Y  (+Z improvement)

### Kept experiments (N):
| # | Score | Δ | What changed |
|---|---|---|---|
| 1 | 62.5 | baseline | baseline |
| 3 | 75.0 | +12.5 | added explicit output format |
...

### Discarded experiments (M):
[list with brief reason]

### Recommendations for next session:
- [top 3 remaining ideas worth trying]
```

---

## Example: Improving a Claude Skill Overnight

**Setup:**
- Artifact: `/mnt/skills/user/n8n-workflow-patterns/SKILL.md`
- Test prompts: 20 real-world n8n questions
- Metric: % answered correctly by Claude using only the skill
- Baseline: run all 20 prompts → score first

**Typical first-session trajectory:**
1. Baseline: 60% → keep
2. Add concrete workflow examples: 72% → keep
3. Add "common mistakes" section: 65% → discard
4. Restructure by workflow type: 78% → keep
5. Tighten description trigger language: 80% → keep
6. Add error handling patterns: 83% → keep
7. Remove redundant preamble: 83% → keep (simpler)
...

Wake up to a skill that went from 60% to 83%+ with a full research log.

**Meta use — improving this skill with itself**: Yes, this is valid and encouraged. The autoresearch-loop skill itself was built and improved using exactly this loop across multiple sessions. Artifact = SKILL.md, metric = pass rate on test prompts that evaluate guidance quality, eval set = prompts covering real edge cases users hit. The only twist: the eval set should test *guidance quality* (does the skill tell Claude what to do correctly?) not just triggering.

---

*Methodology: github.com/karpathy/autoresearch*
