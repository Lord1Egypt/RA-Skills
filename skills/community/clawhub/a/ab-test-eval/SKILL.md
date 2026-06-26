---
name: ab-test-eval
description: "Run A/B evaluation tests for any OpenClaw skill, script, hook, or cron job. Make sure to use this skill whenever the user mentions testing, benchmarking, comparing, or evaluating a skill, script, hook, or cron job — even if they don't explicitly ask for 'AB testing'. Supports 10 eval modes: baseline comparison, regression testing, model-swap, prompt variants, trigger accuracy, adversarial robustness, script validation, hook dry-run, cron dry-run, and integration testing."
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["mkdir", "cp"]
          }
      }
  }
---

# AB Test Eval — Automated Component Benchmarking via Subagents

Evaluate any OpenClaw component (skill, script, hook, cron job) by spawning parallel subagents and comparing arms. Supports multiple eval modes, auto-grading, and regression tracking.

## Step 1: Choose the Eval Mode

Pick the mode that matches the user's intent:

| Mode | Question | Arms |
|------|----------|------|
| **baseline** | Does the skill help at all? | with-skill vs without-skill |
| **regression** | Did changes break anything? | skill-v2 vs skill-v1 |
| **model-swap** | Works on another model? | model-A vs model-B |
| **prompt-variant** | Which description works better? | variant-A vs variant-B |
| **trigger-accuracy** | Dispatches correctly? | should-trigger vs should-not |
| **adversarial** | Robust against bad inputs? | clean vs perturbed |
| **script-test** | Script produces correct output? | script-A vs script-B |
| **hook-dryrun** | Hook responds correctly? | with-hook vs without |
| **cron-dryrun** | Cron payload does the right thing? | cron-run vs baseline |
| **integration** | Full stack works together? | full vs missing-component |

Default to **baseline** if unclear.

## Step 2: Prepare Directory Structure

Create the eval workspace as a sibling to the skill directory:

```
<skill-dir>/evals/evals.json
<skill-dir>/<skill-name>-workspace/
  iteration-1/
    <eval-name>/
      <arm-a>/
        outputs/commands.md
        timing.json
        grading.json
      <arm-b>/
        outputs/commands.md
        timing.json
        grading.json
      eval_metadata.json
    benchmark.json
    benchmark.md
  iteration-2/
    ...
  history.jsonl
```

Create directories with `mkdir -p`. Use descriptive arm names (e.g. `with_skill`, `without_skill`, `new_version`, `old_version`).

## Step 3: Define or Generate Evals

### If evals already exist
Read `<skill-dir>/evals/evals.json` and present the cases to the user for confirmation before running. Do not auto-run without sign-off.

### If evals are missing
Generate them by reading the skill's `SKILL.md` and creating 4-6 realistic eval cases:

1. **Happy path** — clear request the skill should nail
2. **Ambiguous request** — could go multiple ways
3. **Edge case** — unusual params or corner case
4. **Negative case** — similar but should NOT trigger this skill
5. **Multi-step case** — complex multi-tool request
6. **Adversarial case** (if mode=adversarial) — misleading / typo / injected junk

Write to `<skill-dir>/evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user request",
      "expected_output": "What correct behavior looks like",
      "files": []
    }
  ]
}
```

Then show them to the user: *"Here are the test cases I plan to run. Do these look right, or do you want to add more?"*

Wait for approval before spawning subagents.

## Step 4: Efficiency Controls — Dry-Run Preview & Smoke Test

Before spawning expensive subagents, offer the user two efficiency controls (especially useful when eval count > 3 or arms > 2).

### `--dry` Preview
Generate a **preview report** that lists exactly what will run, without spawning any subagents:

```markdown
# Eval Preview Report
- Mode: baseline
- Evals: 4
- Arms per eval: 2 (with-skill, without-skill)
- Model: current
- Estimated subagent calls: 8

Evals:
1. happy-path-basic — 2 arms, 3 assertions
2. ambiguous-request — 2 arms, 3 assertions
```

Present this to the user and ask: *"This looks like X evals across Y arms. Should I proceed, or do you want to trim the list?"*

### `--smoke` Smoke Test
If the user wants a quick confidence check, run **only the first eval** end-to-end (all arms + grading). This verifies the pipeline works before committing to the full run.

After a successful smoke test, ask: *"Smoke test passed. Should I run the remaining N evals now?"*

## Step 5: Write Assertions

While waiting for user approval (or while subagents run), draft assertions in `eval_metadata.json` for each eval.

Save to `<workspace>/iteration-N/<eval-name>/eval_metadata.json`:

```json
{
  "eval_id": 1,
  "eval_name": "happy-path-basic",
  "prompt": "The user's task prompt",
  "assertions": [
    {
      "text": "Uses the --force flag",
      "expected": true
    },
    {
      "text": "Warns about OAuth timeout gotcha",
      "expected": true
    }
  ]
}
```

Assertions use `text` and `expected` fields. These are the basis for grading.

## Step 6: Spawn Subagents in Parallel

For **each eval**, spawn all arms in the same turn. Launch as many as the environment allows concurrently.

### Baseline mode
- **with_skill**: load `SKILL.md`, execute prompt, save outputs
- **without_skill**: same prompt, no skill, save outputs

### Regression mode
- **new_skill**: load updated `SKILL.md`
- **old_skill**: load a snapshot of the previous version (make a `cp -r` snapshot before editing)

### Model-swap mode
- **model-a**: run with skill + model A override
- **model-b**: run with skill + model B override

### Prompt-variant mode
- **variant-a**: load skill variant A's `SKILL.md`
- **variant-b**: load skill variant B's `SKILL.md`

### Trigger-accuracy mode
Each prompt gets ONE subagent tasked as the dispatcher:
> "You are the dispatcher. Given this user prompt, would you load `<skill-path>/SKILL.md` before responding? Answer yes/no and explain why."
Save yes/no explanations, then grade TP/FP/TN/FN.

### Adversarial mode
- **clean**: normal prompt + skill
- **perturbed**: prompt with typos / injected irrelevance / misleading framing + skill

### Script-test mode
- Run the bundled script with controlled inputs and assert on stdout, exit code, and generated files.
- Arms can be: **current-script** vs **previous-script**, or **script-with-skill-guidance** vs **naive-approach**.
- Assertions focus on correctness, idempotency, and edge-case handling.

### Hook-dryrun mode
- **Simulate** a hook event by spawning a subagent and telling it: "Pretend you are an OpenClaw agent receiving a `<hook-type>` event with this payload. Given this hook's `SKILL.md` or config, what would you do?"
- Do NOT modify actual system hook registrations. This is a read-only simulation.

### Cron-dryrun mode
- Extract the cron job's payload (task command or script path from `jobs.json` or cron config).
- Run the payload in an isolated subagent or `exec` dry-run context.
- Assert on expected side effects, file outputs, or command sequence.
- Also verify the cron expression is valid and produces expected schedule times.

### Integration mode
- Test the **full stack**: user prompt → skill dispatch → script execution → hook response.
- Arms: **full-stack** vs **missing-script** vs **missing-hook** vs **skill-only**.

**Task template for standard arms:**

```
Execute this task:
- Arm: <arm-name>
- Skill path: <absolute-path> or "none"
- Model override: <model> or "default"
- Task: <eval prompt>
- Input files: <files or "none">
- Save outputs to: <workspace>/iteration-N/<eval-name>/<arm>/outputs/commands.md
- Execute the task using available tools — if the subagent has tool access, run commands for real; if not, document what would be done.
```

## Step 7: Capture Timing from Notifications

When each subagent completes, its notification includes `total_tokens` and `duration_ms`. **This is the only chance to capture it.**

Save to `<arm>/timing.json`:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Process each notification as it arrives rather than batching.

## Step 8: Auto-Grade with LLM-as-Judge

Spawn a **grading subagent** per eval to compare all arms against the assertions:

```
Read the following files:
- <workspace>/iteration-N/<eval-name>/<arm-a>/outputs/commands.md
- <workspace>/iteration-N/<eval-name>/<arm-b>/outputs/commands.md

Eval prompt: <prompt>
Expected output: <expected_output>

Grade each arm against these assertions:
<assertions from eval_metadata.json>

For each arm, save a separate grading.json with:
- A top-level "expectations" array with text/passed/evidence
- A "summary" with passed/failed/total/pass_rate

Save arm A results to: <workspace>/iteration-N/<eval-name>/<arm-a>/grading.json
Save arm B results to: <workspace>/iteration-N/<eval-name>/<arm-b>/grading.json
```

Each `grading.json` schema:

```json
{
  "expectations": [
    {
      "text": "Uses the --force flag",
      "passed": true,
      "evidence": "Output contains 'clawhub update --force'"
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 0,
    "total": 3,
    "pass_rate": 1.0
  }
}
```

For trigger-accuracy runs, save a separate `trigger_grading.json` with `tp`, `fp`, `tn`, `fn` tallies at the eval level.

## Step 9: Aggregate and Generate Report

Write `benchmark.json`:

```json
{
  "metadata": {
    "skill_name": "my-skill",
    "mode": "baseline",
    "model": "current-model-id",
    "timestamp": "2026-04-11T05:30:00+08:00",
    "evals_run": [1, 2, 3],
    "arms": ["with_skill", "without_skill"]
  },
  "evals": [
    {
      "eval_id": 1,
      "eval_name": "happy-path-basic",
      "arms": {
        "with_skill": {
          "pass_rate": 1.0,
          "passed": 3,
          "total": 3,
          "tokens": 12345,
          "duration_seconds": 17.6
        },
        "without_skill": {
          "pass_rate": 0.67,
          "passed": 2,
          "total": 3,
          "tokens": 18590,
          "duration_seconds": 29.0
        }
      }
    }
  ],
  "totals": {
    "with_skill": { "pass_rate": 0.85, "passed": 17, "total": 20 },
    "without_skill": { "pass_rate": 0.45, "passed": 9, "total": 20 }
  },
  "delta": {
    "pass_rate": "+0.40"
  },
  "notes": [
    "Arm with_skill consistently better on safety assertions",
    "eval-3 edge-case shows no difference — consider strengthening skill"
  ]
}
```

Append a compact line to `history.jsonl` for regression tracking.

Then write `benchmark.md` with:
- Executive summary (delta, winner, biggest weaknesses)
- Per-eval breakdown table
- Notable failures with quotes
- Recommendations for improving the skill

Present the summary to the user directly in chat.

## Step 10: Iterate Based on Feedback

1. Discuss results with the user
2. Improve the skill based on failed assertions
3. Rerun into `iteration-(N+1)/`
4. Compare `history.jsonl` entries for trend
5. Repeat until satisfied

## Mode-Specific Notes

- **Regression**: Snapshot old skill before editing (`cp -r`). Use previous version as baseline.
- **Model-swap**: Use `sessions_spawn` with `model` override.
- **Prompt-variant**: Create two temp skill copies with different descriptions.
- **Trigger-accuracy**: Generate 10 queries (5 should-trigger, 5 near-miss should-not). Grade precision/recall/F1.
- **Adversarial**: Perturbations include typos, irrelevant context injection, misleading framing. Report degradation score = clean_avg - perturbed_avg.
- **Script-test**: Run via `exec` for deterministic results unless script invokes LLM. Check happy-path AND error handling.
- **Hook-dryrun**: Simulate event via subagent with exact payload JSON. Do NOT modify actual hook registrations.
- **Cron-dryrun**: Validate cron expression and list next N execution times. If payload sends messages, use dry-run constraint.
- **Integration**: For missing-component arms, tell subagent: "You do NOT have access to <component X>."

## Hard Constraints

- **Do not auto-run evals without user sign-off** — present evals and wait for approval before spawning
- **Respect `--dry` and `--smoke`** — offer preview / smoke-test paths to improve UX and reduce wasted tokens
