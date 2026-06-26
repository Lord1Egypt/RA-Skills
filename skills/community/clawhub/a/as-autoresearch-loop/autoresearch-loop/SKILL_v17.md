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
- **The artifact is a one-time document** (a single client proposal, a one-off report) — the loop is for artifacts that will be reused and improved over time. A one-time deliverable has no future eval value; just write it well directly

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

**Warm-starting from a related artifact**: If a similar artifact already exists (e.g., a Barcelona property agent prompt when you need a Madrid one), start from it rather than from scratch — it inherits solved problems and gives a better baseline than an empty file. But: you must still run a proper baseline (iteration 0) on the new artifact with a new, context-appropriate eval set. Don't assume the old score transfers. Early experiments may show fast gains just from removing Barcelona-specific content before the real Madrid-specific improvements begin.

**Live production artifacts**: If the artifact is currently serving real users (a live agent, a deployed workflow), never run the loop on the live version directly. Instead: (1) copy it to a working branch/file, (2) freeze the live version — no changes until the loop produces a winner, (3) run the loop on the copy, (4) do a deliberate controlled deploy of the winning version when ready. The metric can't catch production regressions in real-time; protect live users by keeping the loop sandboxed.

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

**Multi-model artifacts** — if the artifact must work across different models (e.g., Opus and Sonnet), ONE METRIC still applies. Options: (a) **floor strategy** — use the weaker model's score as the metric, ensuring the artifact works everywhere; (b) **usage-weighted average** — weight by actual usage distribution (e.g., `0.3 * opus_score + 0.7 * sonnet_score` if most users are on Sonnet). Lock the model weights before the loop starts, same as composite metric rules. Do not run separate loops on the same artifact for different models — that creates conflicting optimization pressures.

### 3. The Budget (Experiment Scope)
What one experiment consists of. Keep it short — Karpathy uses 5 minutes per training run. Translate to your domain:

- Skill: run N test prompts through Claude (N = 5–20; use a fast subset for iteration, the full set before committing a keep on borderline results)
- Workflow: execute on M sample inputs
- Process: dry-run or peer review against checklist

**What makes a good eval set:**
- **Diverse** — covers all the main use cases of the artifact, not just the happy path
- **Adversarial** — includes inputs that should fail gracefully, edge cases, ambiguous inputs
- **Stable** — prompts that have clear, unambiguous pass/fail criteria; avoid prompts where "it depends"

**If a prompt's criteria turn out ambiguous mid-loop**: You cannot change the prompt (EVAL IS IMMUTABLE), but you CAN clarify the scoring rubric — the prompt text is fixed, but if the criteria were genuinely underspecified (e.g., "respond appropriately"), document a concrete interpretation now and apply it consistently for the rest of the session. Flag this prompt for replacement in the next session's eval set. Never define "pass" after seeing the output for that specific run.
- **Representative** — if the artifact handles 5 different scenarios, have prompts for each
- **Large enough** — with fewer than 10 prompts, one flip = 10–17 percentage points. That's noise, not signal. Require at least 10 prompts; with fewer, require 2+ prompt improvements (not 1) before keeping an experiment.

A bad eval set (10 nearly identical prompts) will give you a misleadingly high score. If you improve from 60% to 80% but all 8 passing prompts are the same scenario, you've learned nothing about the other scenarios.

**Building an eval set from scratch** — if none exists:
1. List every distinct use case and scenario the artifact is supposed to handle
2. For each scenario, write 1–2 prompts: one normal case, one edge/adversarial case
3. Aim for 10–20 prompts total — enough for meaningful signal, small enough to run fast
4. Write the pass/fail criteria for each prompt BEFORE running any experiments — don't define "pass" after seeing the output
5. If you have real historical inputs (e.g., past emails, past requests), use those as the foundation — they're more realistic than synthetic ones

Do not start the loop until the eval set is complete and criteria are written.

**Evolving the eval set across sessions** — how to make each round harder without adding random prompts:
1. After each session, review every prompt that passed easily (especially ones that passed from round 1). Ask: "What harder version of this question would break the current artifact?"
2. Find scenarios the artifact handles correctly but only barely — probe the edge of what it knows
3. Add failure modes one step removed from current coverage: if it handles "email in Spanish," test "email mixing Spanish and Catalan"
4. Retire prompts that have become trivial — they no longer discriminate between good and bad versions
5. Each new eval set should feel noticeably harder than the last. If you can't design harder prompts, the artifact has genuinely converged
6. **Regression suite**: When retiring old prompts, keep 1–2 of the most critical from each round in a small, persistent "regression suite" that runs alongside (not instead of) each new round's eval. This prevents cross-round forgetting — a capability that passed in Round 2 can silently break in Round 6 if no current eval tests it. The regression suite grows slowly (aim for 5–10 prompts max) and acts as a guardrail, not a scoring mechanism — a regression failure is a red flag to investigate, not an automatic discard

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

**Diagnostic pass at low baselines**: If the baseline is below ~50% and you have no prior experiment history, do NOT jump straight into changes. First, read every failing prompt carefully and categorize why it fails — missing concept, wrong structure, too vague, wrong tone, etc. Group the failures into 2–3 root cause buckets. Your first experiment should address the largest bucket. Experimenting without this diagnosis wastes iterations on symptoms rather than causes.

**Escalation rule**: If 8+ consecutive experiments discard on incremental changes, escalate to a radical rewrite of the artifact. One big structural change is still one experiment. If it discards, your backup brings you right back.

**Simplicity criterion (from Karpathy)**: All else equal, simpler is better.
- A 2% improvement with 30 new lines: probably not worth it
- A 2% improvement by deleting 10 lines: definitely keep
- 0% change but much cleaner: keep the simpler version

**Artifact size creep**: Over many rounds, each harder eval demands more content — the artifact grows monotonically even with simplification passes. Countermeasures: (1) set a **hard size budget** (max line/token count) at campaign start; when approaching it, the next experiment must be a compression refactor, not an addition; (2) prefer **structural compression** over line-by-line trimming — replace 5 specific examples with 1 generalized pattern, merge overlapping sections, extract repeated guidance into a shared rule; (3) if the artifact genuinely needs 400+ lines to pass a hard eval, it's likely too broad in scope — split it into two focused artifacts with separate loops. Size discipline is a long-campaign survival skill, not just an aesthetic preference.

### Step 4: Running the Evaluation

**Handling noisy metrics**: LLM-based evaluations are non-deterministic — the same artifact can score 74% one run and 81% the next. Strategies:
- **Multi-run averaging**: Run the eval 3 times, take the mean. Require improvement > the noise floor (e.g., +5%) before keeping.
- **Noise floor rule**: If your runs vary by ±7%, a +3% improvement is meaningless — it's within noise. Only keep changes that beat the noise floor.
- **Deterministic scoring**: Use pass/fail rubrics with binary criteria where possible — they're less noisy than 1–5 scales.

If your eval is highly noisy, averaging 3 runs before deciding keep/discard is the minimum. Treat single-run scores with suspicion.

**LLM-as-judge**: When human scoring is impractical (too many prompts, too slow), using an LLM evaluator is viable but introduces specific risks. Mitigate: (a) use binary pass/fail with very explicit, observable criteria — subjective rubrics ("respond appropriately") amplify LLM inconsistency; (b) fix the evaluator model for the entire loop — switching between Opus and Sonnet as judge mid-loop is a form of metric drift; (c) periodically spot-check a sample of LLM judgments against your own human scoring — if agreement drops below ~85%, the rubric needs tightening, not the judge. LLM-as-judge adds noise; treat it like noisy metrics (multi-run averaging, noise floor rule) and don't trust single-run borderline results.

**Suspiciously large gains**: A single experiment producing +30–40% improvement warrants re-running the eval before logging a keep. Normal experiments produce +5–15%; a large jump suggests either a fundamental structural fix (legitimate) or a measurement error (e.g., eval ran differently, wrong file loaded). Re-run once to confirm. If it reproduces, it's real — log and celebrate. If it doesn't, treat as noise.

**For Claude Skills:**
Take the test prompts provided (or generate them). For each prompt:
1. Load the skill SKILL.md into context
2. Follow the skill to complete the task
3. Score against the rubric (pass/fail or 0–100)
4. Average across all prompts = the metric

**For n8n Workflows, System Prompts, Business Processes:**
Adapt the same pattern: run the artifact against fixed inputs, score each against the rubric, average. For workflows, trace node-by-node; for system prompts, use a fixed adversarial+normal prompt set; for SOPs, check against a requirements checklist.

### Step 6: Keep or Discard

| Condition | Action |
|---|---|
| Score strictly improved | **KEEP** — advance to next iteration from this version |
| Score equal or worse | **DISCARD** — revert artifact to previous version |
| Evaluation errored | **ERROR** — log, investigate, fix or skip |

On discard: restore the artifact to its previous state before trying the next experiment.

**Internal contradictions override the metric**: If a kept experiment introduces conflicting instructions within the artifact (e.g., "always use bullets" in one section, "always use prose" in another), revert it — a higher score achieved through a broken artifact is not a genuine improvement. Fix the contradiction as its own targeted experiment, then re-run. Structural integrity of the artifact is a hard constraint that the metric alone cannot enforce.

**Regression risk**: The metric is only trustworthy if your eval set is well-designed. If you notice the artifact seems worse at something NOT in your eval set (e.g., it now handles Spanish inputs poorly), treat that as a red flag. You have two options: discard the change on principle, or note the gap and add a Spanish-language prompt to the NEXT session's eval set. The metric is king — but only if it measures the right things.

**Metric gaming / Goodhart's Law**: "When a measure becomes a target, it ceases to be a good measure." After 20–30 experiments, high scores (95%+) on a fixed eval set may reflect overfitting to those specific prompts rather than genuine improvement. Signs: score is high but real-world performance feels flat. Fix: redesign the eval set for the next session with harder, more diverse prompts. The loop is only as good as its yardstick.

**Eval isolation**: If the artifact being improved can read the eval prompts during experiments (e.g., they're in the same folder and Claude loads both), you've created a structural overfitting risk — the artifact is being tuned to specific question wording, not underlying capability. Keep eval files in a separate location not loaded during artifact editing, or run scoring as a distinct step where the artifact doesn't see the questions. Eval criteria visible during scoring = fine. Eval questions visible during modification = problem.

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

**Verify revert completeness**: After reverting, always confirm the file matches the backup before proceeding. If uncertain whether a discard was fully reverted: diff the current file against the backup (`diff SKILL.md SKILL_v3.md`), or run the eval immediately — if the score matches the last logged keep score, the state is clean. Do NOT continue on uncertain state. Contamination is insidious: subsequent experiments build on a corrupted baseline, making all future results unreliable.

Log the discard entry in results.tsv BEFORE reverting, so the history is complete.

If you're using git: `git stash` or `git checkout -- <file>` works just as well. The key is that you always have a clean last-known-good to return to.

**Version file cleanup**: After many sessions you may accumulate dozens of numbered backups. You only need two at any time: the baseline (v0) and the current best. Once results.tsv documents what each version contained, intermediate files can be archived or deleted — the log is the history, not the files. If using git, commit after every KEEP and delete numbered copies entirely; the commit log replaces them.

**If you forgot to save a backup**: Check git history first (`git log --oneline`). If not tracked, read results.tsv to identify what the last kept version looked like from its description, then reconstruct those changes manually from the log. This is painful — it's why you back up immediately after every KEEP, before running the next experiment.

**If results.tsv is corrupted or lost**: The current best artifact is more important than the log — don't start over. Reconstruct what you can: diff the baseline (v0) against the current best to see the net changes across all sessions. Add a note in results.tsv marking the gap (e.g., "iterations 5–12 lost — see diff of v0 vs v12 for net changes"). Continue from the next iteration number. What you lose: research memory for the missing entries, which means you might re-try already-failed experiments and can't trace why specific content was added. What you keep: all artifact improvements already achieved. The log is valuable, but the artifact is the deliverable.

---

## Rules

**EVAL IS IMMUTABLE**: Once the loop starts, the test set and scoring rubric cannot change. Adding, removing, or modifying eval prompts mid-loop invalidates all previous scores — you can no longer compare iterations fairly. If you discover a missing edge case, note it for the next session's eval set. Don't touch the current one.

**Contradictory eval prompts**: If you discover two prompts with conflicting pass criteria mid-loop (e.g., one requires bullets, another requires prose), you cannot fix them without invalidating the current session. Finish the session, note the contradiction, and redesign the eval for next session with it resolved. Log your scores honestly — they're partially meaningless against a contradictory eval, but the experiment history still has value. For future eval design: read every prompt pair for logical conflicts before starting a loop.

**Metric drift from external changes**: If the underlying source of your metric changes between sessions — e.g., a compliance checklist is updated, an API spec changes, a rubric is revised — your old results.tsv scores are no longer comparable. Treat this like a new loop: archive the old results.tsv as historical record, run a fresh baseline (iteration 0) against the updated metric, and continue from there. Do not add experiments to the old log.

**Input distribution drift**: If the real-world inputs your artifact handles have changed significantly (e.g., your eval was built on emails from 6 months ago and client communication style has evolved), the eval set no longer represents reality — even if the scoring criteria haven't changed. Pause the loop, rebuild the eval set from recent real inputs, establish a new baseline. This is distinct from metric drift: the *criteria* are the same, but the *test cases* are stale. Same cure: fresh eval set, fresh session.

**NO SCOPE CREEP**: The artifact's purpose cannot expand mid-loop. If you started improving a consulting SOW template and realize it should also cover retainer agreements, that's a scope change — not a content improvement. The existing eval set doesn't test the new scope, so any score change is meaningless. Finish the current loop for the original scope. Start a fresh loop with a new eval set for the expanded scope.

**BASELINE FIRST**: Iteration 0 is always a zero-change run. Do not modify the artifact. Run the evaluation as-is to establish the baseline score. Every future experiment is compared against this number. Without a clean baseline, you have nothing to beat.

**If the baseline looks broken** (e.g., 10% on a reasonable eval set): do NOT start experimenting from there. Investigate first — is the eval set miscalibrated? Is the artifact fundamentally broken before you started? Is the scoring rubric too strict? Fix the root cause (artifact or eval), then re-run the baseline as a clean iteration 0. Experimenting on top of a broken baseline wastes every experiment on debugging rather than improvement.

**NEVER STOP (mid-session)**: Once the loop starts, do not pause to ask the user if you should continue. The human might be away. Run until manually interrupted. If you run out of ideas, think harder — look at failed test cases, try the inverse of something that worked, try combining near-misses, escalate to a radical rewrite.

**Stopping for the day is fine**: "Never stop" means don't pause mid-session to ask permission. It does not mean you can never end a work session. When the human says they're done for the day: save the best artifact version, ensure results.tsv is up to date, note the top 2–3 experiment ideas to try next session. Resume tomorrow using the Resuming a Session guide. The loop continues across sessions — it doesn't reset.

**Principled stopping criteria**: "Never stop" applies mid-session, but a loop can legitimately run its course. Consider stopping when ALL of these are true: (1) score ≥ 95% on a well-designed, diverse eval set, AND (2) 10+ consecutive discards across incremental, structural, and radical experiments, AND (3) you've already tried combining near-misses. At that point the eval set — not the artifact — is likely the bottleneck. Redesign the eval and start a fresh session.

**The 100% score**: If you genuinely hit 100% on a diverse, adversarial eval, run one simplification pass first — try removing sections to see if you can maintain 100% with less content. If simplification discards, you've confirmed the artifact needs everything it has. Then stop: you've converged. 100% is only meaningful if the eval was hard; a shallow eval gives false 100%s.

**The good-enough decision**: At high scores (90%+), apply a cost/benefit lens. If the remaining failing prompts cover rare edge cases that almost never appear in practice, 92% may be genuinely good enough to ship — don't optimize for the last 8% if it has no real-world impact. If the failing prompts cover common scenarios, keep going. The loop is a tool, not a religion.

**When the baseline starts high (95%+)**: The artifact may already be at or near its ceiling before the loop begins. Run 3–5 simplification experiments first — can you achieve the same score with less content? If those discard, try 2–3 targeted improvements on failing prompts. If those also discard, the loop has served its purpose in one session: the artifact was already good, simplification didn't help, and there's no obvious improvement to find. Ship it.

**Experiment cost**: Each experiment has a real time cost. If experiments are expensive (30+ minutes each), apply a tighter diminishing-returns threshold — don't run 10 more experiments chasing a 2% gain when that time is worth more elsewhere. After 3–4 consecutive discards at high scores, consider pausing, stepping back, and either redesigning the eval set or declaring good enough. Cheap experiments (5 minutes) warrant more persistence; expensive ones demand more selectivity.

**ONE CHANGE AT A TIME**: Never bundle two *untested* hypotheses in one experiment. You won't know which one caused the result.

**Exception — combining near-misses**: If change A was tested and discarded (0% improvement) AND change B was tested and discarded (0% improvement), you may combine them in one experiment. The logic: individually they had no effect, so combining them can't be blamed on bundling. If the combo works, you accept not knowing which part drove it — that's fine. If it discards, revert to best-so-far as usual.

**ONE METRIC**: Pick exactly one metric before the loop starts and never change it. Two metrics create unsolvable keep/discard decisions — if one improves and one degrades, you're stuck. If you care about multiple dimensions, define a single weighted composite score before starting, not mid-loop.

**When human intuition conflicts with the metric**: If the metric says discard but you prefer the result, the metric wins — overriding it mid-loop breaks the entire comparison system. The right response: discard per the metric, then note your intuition as a hypothesis ("felt clearer") and design a future experiment that specifically targets that dimension. If your intuition is consistently right and the metric keeps being wrong, the metric is poorly designed — redesign it for next session, don't override it now.

**ONE ARTIFACT**: The loop improves exactly one artifact per session. Two artifacts (e.g., a system prompt AND the workflow that calls it) means you can't isolate what caused a score change. Finish one loop, ship it, then start a fresh loop for the next artifact.

**Artifact dependencies**: If an artifact depends on another (e.g., a routing skill fed by a language detection skill), and performance is bad — isolate which one is broken before starting any loop. Test the upstream artifact in isolation first. Starting a loop on the downstream artifact while its inputs are broken means you're optimizing against corrupted data. Fix root causes before iterating.

**Parallel loops are fine**: One artifact per loop, but you can run multiple loops simultaneously on *different* artifacts with separate eval sets and separate results.tsv files. The constraint is isolation within a loop, not globally.

**Same-artifact parallel branching**: Running two experiments from the same baseline and picking the winner is valid — *if* you fully discard the loser and continue from the winner only. What's not valid: merging both into one artifact ("take the best of both"). That's bundling two untested changes and you lose isolation. Pick one winner, discard the other entirely, continue.

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

**Handing off to another person**: If someone else is taking over the loop (e.g., a colleague picking up mid-run), give them:
1. `results.tsv` — the full experiment history
2. The current best artifact version (last `keep` entry)
3. The fixed eval set + scoring rubric (unchanged)
4. A short note: current best score, top 2–3 ideas not yet tried, any patterns observed in failures

They continue from the next iteration number — no re-running baseline, no restarting from scratch.

---

## Applying to Specific Artifact Types

Quick reference for good experiment ideas by type:

**Claude Skills**: add concrete examples, add "when not to use" section, strengthen trigger language, add edge case handling, reorder sections for clarity, add quick-reference tables

**n8n Workflows**: simplify multi-step logic into fewer nodes, add error handling branches, fix expression syntax, improve routing conditions, add validation before expensive operations

**System Prompts**: tighten instruction specificity, add formatting constraints, add failure mode handling, add few-shot examples, remove contradictory instructions

**Business Processes / SOPs / Team Workflows**: eliminate redundant steps, add decision trees for edge cases, add rollback/error procedures, clarify ownership, add measurable completion criteria. When the "artifact" has no single file (team workflows where people are the execution layer), the artifact becomes the process documentation (SOP, RACI, checklist) and the eval becomes structured simulation against case studies — the loop is identical, experiments just take longer.

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

**Delivering to a client when the loop has converged**: If the loop is genuinely done (high score, consecutive discards, tried everything), the deliverable package is: the best artifact version + results.tsv + eval set. Frame it professionally: "We ran N experiments over X sessions, improved from Y% to Z% on a [diverse/adversarial] eval set, and reached a performance ceiling after [M] consecutive non-improving experiments. The artifact is production-ready." The results.tsv is your audit trail — it shows rigorous, evidence-based iteration, not guesswork.

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

**Cross-artifact learning**: After running multiple loops on similar artifact types (e.g., several SKILL.md files), common improvement patterns emerge — add examples, tighten trigger language, add edge case handling. Maintain a living **cross-artifact learnings doc**: a list of "experiments that improved multiple artifacts of this type." Use it as the warm-start hypothesis list for each new loop of the same type — this can cut early-session iteration counts dramatically. The artifact warm-starts from a related file; the experiment ideas warm-start from prior loop history.

**Meta use — improving this skill with itself**: Yes, this is valid and encouraged. The autoresearch-loop skill itself was built and improved using exactly this loop across multiple sessions. Artifact = SKILL.md, metric = pass rate on test prompts that evaluate guidance quality, eval set = prompts covering real edge cases users hit. The only twist: the eval set should test *guidance quality* (does the skill tell Claude what to do correctly?) not just triggering.

**When to retire an artifact from active improvement**: The loop is not a continuous obligation. Retire it when: (a) the artifact handles all real-world use cases reliably in practice, and (b) you genuinely struggle to design harder eval prompts because there are no obvious gap scenarios left. At that point, don't run more sessions — ship it and maintain it. Resume a loop session only when real-world usage reveals a new failure mode worth addressing. The goal is a useful artifact, not a perfect score on an ever-harder eval set.

---

*Methodology: github.com/karpathy/autoresearch*
