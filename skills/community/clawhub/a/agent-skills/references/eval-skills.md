# Skill Quality Evaluation

Use structured evals to validate skill quality.

## Test Case Design

```json
{
  "id": 1,
  "prompt": "what a real user would say",
  "expected_output": "what success looks like",
  "files": ["evals/files/input.csv"],
  "assertions": ["verifiable assertion 1", "assertion 2"]
}
```

- Start with 2-3 test cases, don't over-invest
- Vary prompts: formal/casual/typos/different detail levels
- Cover edge cases: malformed input, ambiguous instructions
- Use realistic context: file paths, column names, etc.

## Running Evals

Run each test case twice: **with skill** + **without skill** (baseline). Workspace structure:

```
workspace/iteration-1/
├── eval-01/with_skill/{outputs,timing,grading}
├── eval-01/without_skill/{outputs,timing,grading}
└── benchmark.json
```

Record `timing.json`: `{"total_tokens": 84852, "duration_ms": 23332}`

## Assertions

Good: programmatically verifiable ("output file is valid JSON"), specific and observable ("chart has labeled axes"), countable ("≥3 recommendations").

Weak: too vague ("output is good"), too brittle ("must use exact phrase X").

## Grading

Each assertion PASS/FAIL + concrete evidence (quote/reference output):

```json
{"assertion_results": [{"text": "...", "passed": true, "evidence": "Found chart.png"}],
 "summary": {"passed": 3, "failed": 1, "total": 4, "pass_rate": 0.75}}
```

Grading principles: PASS needs concrete evidence, no benefit of doubt. Also review assertions themselves for reasonableness.

**Blind comparison** (comparing versions): LLM judge scores without knowing which version is which.

## Aggregation

```json
{"run_summary": {
  "with_skill": {"pass_rate": {"mean": 0.83}},
  "without_skill": {"pass_rate": {"mean": 0.33}},
  "delta": {"pass_rate": 0.50}
}}
```

Delta tells you the skill's cost (time/tokens) vs. benefit (pass rate improvement).

## Pattern Analysis

- Remove assertions both sides pass (no signal)
- Investigate both-side failures (broken assertion or too-hard case)
- Study skill-passes / no-skill-fails (where skill adds value)
- Inconsistent results → ambiguous instructions, add examples or specifics
- Check timing/token outliers

## Human Review

Things assertions miss: writing style, visual design, "does it feel right". Record specific actionable feedback.

## Iteration Loop

1. Feed all eval signals + current SKILL.md to LLM for improvement proposals
2. Review and apply changes
3. Rerun all test cases in iteration-N+1/
4. Grade and aggregate
5. Human review. Repeat.

Stop: satisfied / feedback consistently empty / no meaningful improvement.

Guidance for LLM: generalize feedback (not narrow patches), keep lean (fewer better instructions > exhaustive rules), explain why, bundle repeated work into scripts.
