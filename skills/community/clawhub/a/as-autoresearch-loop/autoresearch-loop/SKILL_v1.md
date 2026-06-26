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

### 3. The Budget (Experiment Scope)
What one experiment consists of. Keep it short — Karpathy uses 5 minutes per training run. Translate to your domain:

- Skill: run N test prompts through Claude (N = 5–20)
- Workflow: execute on M sample inputs
- Process: dry-run or peer review against checklist

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

Each experiment should test **one hypothesis**. Think like a researcher:

> "If I add explicit failure mode handling to the skill, the pass rate will increase because the model will know what to do when inputs are malformed."

Good experiment ideas (in rough priority order):
- Fix an obvious gap identified from failed test cases
- Add/improve examples in the artifact
- Restructure for clarity (reorder sections, add headers)
- Tighten or relax constraints
- Add edge case handling
- Simplify — remove something and check if it still works
- Strengthen the description/trigger language
- Add a new section for an underserved use case

**Simplicity criterion (from Karpathy)**: All else equal, simpler is better.
- A 2% improvement with 30 new lines: probably not worth it
- A 2% improvement by deleting 10 lines: definitely keep
- 0% change but much cleaner: keep the simpler version

### Step 4: Running the Evaluation

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

### Step 7: Logging

Always log before the next iteration starts. Never commit a `results.tsv` change without a corresponding artifact state (keep a backup of each "kept" version as `artifact_vN.md` or similar).

---

## Rules

**BASELINE FIRST**: Iteration 0 is always a zero-change run. Do not modify the artifact. Run the evaluation as-is to establish the baseline score. Every future experiment is compared against this number. Without a clean baseline, you have nothing to beat.

**NEVER STOP**: Once the loop starts, do not pause to ask the user if you should continue. The human might be away. Run until manually interrupted. If you run out of ideas, think harder — look at failed test cases, try the inverse of something that worked, try radical restructuring, try combining two previous near-misses.

**ONE CHANGE AT A TIME**: Never bundle two hypotheses in one experiment. You won't know which one caused the result.

**TRACK LINEAGE**: Each experiment builds on the best-so-far, not the original baseline. You are walking uphill.

**TIMEOUT/ERROR HANDLING**: If an evaluation errors or produces unusable results, log it as `error`, investigate once, fix if trivial, skip if not. Don't spend more than 2 attempts on a broken experiment before moving on.

**LOG EVERYTHING**: Even bad experiments. Especially bad experiments. The history is your research memory.

---

## Applying to Specific Artifact Types

### Claude Skills (SKILL.md improvement)

Fixed (do not change):
- The test prompt set
- The scoring rubric
- The evaluation procedure

Editable:
- SKILL.md content (description, body, examples, structure)

Metric: pass rate on test prompts (%)

Good experiments for skills:
- Add more concrete examples
- Add a "when NOT to use" section
- Strengthen description trigger language
- Add edge case handling
- Reorder sections for better flow
- Add a quick-reference table

### n8n Workflows

Fixed (do not change):
- Input schema
- External integrations (credentials, APIs)
- Expected output format

Editable:
- Node configuration
- Expression logic
- Routing conditions
- Error handling
- Step order/structure

Metric: execution success rate, step count reduction, latency

Good experiments for workflows:
- Simplify multi-step logic into fewer nodes
- Add error handling branches
- Fix expression syntax issues
- Improve filter/routing conditions
- Add validation before expensive operations

### System Prompts / Agent Instructions

Fixed (do not change):
- The eval prompt set
- Scoring rubric

Editable:
- System prompt content

Metric: instruction-following score on eval set

### Business Processes / SOPs

Fixed (do not change):
- Compliance requirements
- External system constraints
- Checklist of required outcomes

Editable:
- The process document / SOP

Metric: checklist pass rate, clarity score, completeness score

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

---

## Reference: Karpathy's Original Design Choices (Worth Stealing)

1. **Fixed budget per experiment**: Makes experiments comparable regardless of what changed
2. **Single metric**: No multi-objective confusion — one number decides keep/discard
3. **One file to modify**: Keeps scope manageable, diffs reviewable
4. **Self-contained**: No external state between experiments
5. **Never stop**: The human's job is to set the org up, not run it
6. **Simplicity as a first-class criterion**: Complexity has a cost, always
7. **Results log stays untracked** (or separate from artifact): History should be append-only truth, not part of the artifact being optimized

Source: https://github.com/karpathy/autoresearch
