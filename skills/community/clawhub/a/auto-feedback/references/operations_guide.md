# Feedback Loop v2 — Operations Guide

## Modes at a Glance

| Mode | How to Trigger | Extra Inputs Needed |
| :--- | :--- | :--- |
| **Standalone** | `--input`, `--text`, or `--observation` | None |
| **Enhanced** | Add `--outcome` flag | `outcome_report.json` from dark-factory |
| **Full Triad** | Add `--outcome` + `--spec` flags | Both `outcome_report.json` and `specification.json` |

The skill auto-detects the mode from the arguments you provide. You never need to set a mode flag.

## Running the Self-Improving Loop

The loop works by feeding each run's `updated_observation.json` back into the next run:

```bash
# Cycle 1 — start from any input
python scripts/orchestrator.py --input my_log.json --goal "Achieve 98% pass rate" --output-dir ./cycle1/

# Cycle 2 — continue from the updated observation
python scripts/orchestrator.py --observation ./cycle1/updated_observation.json --output-dir ./cycle2/

# Cycle 3 — and so on
python scripts/orchestrator.py --observation ./cycle2/updated_observation.json --output-dir ./cycle3/
```

Each cycle accumulates regression tests, tracks performance trends, and produces more targeted suggestions.

## Integrating with Dark Factory

When you have a `dark-factory` outcome report, pass it with `--outcome`:

```bash
python scripts/orchestrator.py \
  --outcome path/to/outcome_report.json \
  --goal "Achieve 98% pass rate" \
  --output-dir ./reports/
```

The skill will automatically extract behavioral test results, generated code metrics, and edge cases from the outcome report — no additional configuration needed.

## Integrating with Intent Engineering (Full Triad)

When you have both a `dark-factory` outcome report and an `intent-engineering` specification:

```bash
python scripts/orchestrator.py \
  --outcome path/to/outcome_report.json \
  --spec path/to/specification.json \
  --output-dir ./reports/
```

The skill will:
1. Check performance against the specification's success criteria.
2. Add new regression tests to `updated_specification.json` for the next intent-engineering cycle.
3. Bump the specification version automatically.

## Customizing Scoring

Edit `references/scoring_weights.json` to change how the performance score is calculated. The weights are automatically renormalized if a metric is missing from the observation.

## Customizing Alignment Checks

Edit `references/alignment_values.json` to define your organization's thresholds. The analyzer checks every observation against these values.

## Customizing Suggestion Rules

Edit `references/suggestion_rules.json` to add or modify suggestion rules. Each rule has a Python-evaluable `condition` and a `suggestion` string.

Available variables in conditions:
- `pass_rate` — float 0.0–1.0
- `duration_ms` — float (milliseconds)
- `failure_count` — int
- `regression_detected` — bool

## Troubleshooting

**No metrics extracted from JSON input**
The observer looks for standard field names (`passed`, `failed`, `pass_rate`, `duration_ms`, `total`). If your log uses different names, either rename the fields or pre-process the log before passing it to the skill.

**No metrics extracted from text input**
The observer uses regex patterns to find numbers in plain text. Make sure your text includes explicit numbers (e.g. "18 passed, 2 failed, took 3.2 seconds").

**Alignment score is always 1.0**
This means no thresholds were violated. If you want stricter checks, raise the thresholds in `references/alignment_values.json`.

**Regression detected unexpectedly**
A regression is flagged when the performance score drops by more than 5% vs. the prior cycle. If this is a false positive, check whether the prior cycle's metrics were unusually high (e.g. from a test run with fewer scenarios).
