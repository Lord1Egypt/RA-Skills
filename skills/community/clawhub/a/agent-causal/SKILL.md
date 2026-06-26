---
name: agent-causal
description: "Agent Causal Decision Tool helps you and your AI agents answer one question from experiment data: should we ship this change, keep running the test, or roll it back? Returns structured JSON decisions, key statistics, and audit trails from A/B tests (frequentist + Bayesian), DiD, cohort/segment analysis, and sequential early stopping."
metadata:
  openclaw:
    category: data-science
    version: "0.10.3"
    license: Apache-2.0
    tools: [exec]
    requires:
      bins: [python3, git, pip]
      python_packages: [click, scipy, numpy, pydantic]
    source: https://github.com/ZhuMorris/agent-causal-decision-tool
---

# Agent Causal Decision Tool

A causal decision and audit tool for AI agents. Evaluate product changes using A/B testing, Difference-in-Differences, and sequential early stopping.

**Source:** https://github.com/ZhuMorris/agent-causal-decision-tool

## What is this?

Agent Causal Decision Tool helps you and your AI agents answer one question from experiment data: "should we ship this change, keep running the test, or roll it back?" It takes in simple A/B or rollout summaries and returns a structured JSON decision, key statistics, and an audit record you can store or review later.

Rather than being a full experimentation platform, it is a **decision engine**. You bring the data (from your logs, BI tool, or CSV); it handles the stats, decision logic, and audit trail.

### Why it exists

In many teams, experiment decisions happen in ad hoc spreadsheets or dashboards. People glance at lift, argue about whether the sample size is enough, and sometimes ship features based on noisy or biased results. Agents make this worse if they are wired to react to any small uplift they see.

This tool wraps a few standard methods into one consistent, agent‑friendly interface:

- **Easy-mode dispatcher (`decide`)** — no need to know which statistical method to use. Paste your numbers and it auto-selects A/B, Bayesian, DiD, or planning from your input fields.
- **Frequentist A/B testing** for classic "control vs variant" questions.
- **Bayesian A/B testing** when you want answers like "there is a 93% chance B is better than A" instead of only p‑values.
- **Difference‑in‑differences (DiD)** for quasi‑experiments like staged rollouts or region‑based launches where you cannot randomize perfectly.
- **Cohort / segment breakdown** when an aggregate result is inconclusive — you can slice by user segment to find hidden signals, with Benjamini-Hochberg correction for 4+ segments.
- **Planning and power checks** so you can see if a test is realistic before you start it.
- **Decision audit** so humans can see what the agent did, why it did it, and how strong the evidence really was.
- **External connectors** — pull experiment data directly from PostHog, normalize it, and run a decision in one step. No manual export needed.

The goal is not to replace your analytics stack, but to give agents a small, reliable decision block they can call inside workflows.

### When to use it

Use this tool whenever you or your agents have experiment or rollout results and need a decision you can defend:

- You ran an A/B test and want to know whether to ship, keep running, or reject the variant.
- You're not sure which method to use — let `decide` auto-detect from your numbers.
- You ran an A/B test and it was inconclusive — you want to know if a specific user segment is driving (or diluting) the effect.
- You rolled out a feature to one region or cohort first and want a DiD estimate of impact compared to a similar control group.
- You prefer a Bayesian summary ("95% chance B is better; expected lift 3–5%") to drive thresholds in automated workflows.
- You need an audit trail with experiment period, traffic size, assumptions, thresholds, and warnings so product, data, or risk teams can review agent decisions later.
- You want to plan an experiment (sample size, minimum detectable effect, expected duration) or compare current results to previous experiments to see which wins are robust.
- Your experiment data lives in PostHog — you want to fetch, normalize, and decide without any manual CSV export.

---

## Security Model

This skill runs as a **local CLI tool only**. After one-time setup, it requires no network access.

**Setup (one-time, before first use):**
```bash
# Download the release tarball — no git clone needed
curl -sL https://github.com/ZhuMorris/agent-causal-decision-tool/archive/refs/tags/v0.10.2.tar.gz -o agent-causal.tar.gz
tar -xzf agent-causal.tar.gz
pip install agent-causal-decision-tool-0.10.2/ -q
```


After installation, the `agent-causal` command is available locally. The tool performs only local statistical calculations.

**When network access occurs:** The PostHog connector (`agent-causal connect posthog`) makes outbound HTTPS requests to your PostHog instance only when explicitly invoked — never automatically. If you do not use the connector, no outbound network access is needed at any point.

**No runtime network access during analysis.** The decision engine, audit, and cohort analysis do not make outbound requests.
**Tools used:** `exec` (for running the `agent-causal` CLI commands you specify). Commands are fully hardcoded with no user-supplied strings interpolated into shell execution.
**PostHog token scope:** Use a read-only API token with minimal scopes. Do not use tokens with write or admin permissions.
**Credential handling:** PostHog API credentials are read from env vars (`POSTHOG_API_KEY`/`POSTHOG_PROJECT_ID`) or a local `~/.posthogrc` file — never hardcoded or logged.

---

## Setup

Before using this skill, install the tool (one-time):

```bash
git clone https://github.com/ZhuMorris/agent-causal-decision-tool.git ~/clawd/agent-causal-decision-tool
pip install ~/clawd/agent-causal-decision-tool -q
```

After this, `agent-causal` is available as a local command. No further network access is required.

---

## Agent-Native Actions (JSON-RPC 2.0)

For AI agent integrations, Agent Causal exposes a JSON-RPC 2.0 API over both stdio and HTTP.

### Stdio mode (for OpenClaw, Codex, Claude Code)

```bash
python -m src.api stdio
```

### HTTP mode

```bash
python -m src.api http --port 8000
```

### Actions

| Action | Description |
|--------|-------------|
| `decide` | **Easy-mode dispatcher** — auto-selects A/B, Bayesian, DiD, or planning from your input fields |
| `decide_ab` | Frequentist A/B test (`mode: frequentist`) or Bayesian (`mode: bayesian`) |
| `decide_rollout` | DiD for staged rollouts / quasi-experiments |
| `plan_test` | Experiment planning (sample size, MDE, feasibility) |
| `audit_result` | Full audit of a stored result by ID |
| `save_result` | Persist a decision result to SQLite history |
| `get_result` | Retrieve a stored result by ID |
| `compare_results` | Compare multiple stored experiments |
| `connect` | Fetch experiment data from an external connector (e.g. PostHog) |

### Request format

```json
{
  "jsonrpc": "2.0",
  "method": "decide_ab",
  "params": {
    "mode": "frequentist",
    "input": {
      "control_conversions": 100,
      "control_total": 5000,
      "variant_conversions": 130,
      "variant_total": 5000
    }
  },
  "id": 1
}
```

### Unified response schema

```json
{
  "decision": "ship|keep_running|reject|escalate",
  "recommended_next_action": "Deploy variant — statistical significance achieved with positive lift.",
  "selected_method": "ab_test|bayesian_ab|did|planning",
  "selection_reason": "Why this method was chosen",
  "confidence": "high|medium|low",
  "effect_summary": "Estimated lift: +30.00% (positive)",
  "warnings": [{"code": "LOW_TRAFFIC", "message": "...", "severity": "info"}],
  "limitations": ["No multiple testing correction applied"],
  "audit_summary": "ab_test: Decision",
  "source_metadata": {"connector": "langsmith", "dataset_id": "ds-001"},
  "internal_result": { ... }
}
```

### Error format

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid A/B test inputs",
  "data": {
    "details": [{"field": "control_total", "issue": "must be >= 1"}],
    "request_id": null
  }
}
```

---

## Commands

### Easy-mode Dispatcher (`decide`)

**Don't know which method you need?** `decide` auto-detects from your input fields — no need to pick the right command:

```bash
# A/B test (auto-detected)
PYTHONPATH=. python3 -m src.cli decide --control 100/5000 --variant 130/5000
PYTHONPATH=. python3 -m src.cli decide --control 100/5000 --variant 130/5000 --format text

# Bayesian A/B (--bayesian flag)
PYTHONPATH=. python3 -m src.cli decide --control 100/5000 --variant 130/5000 --bayesian

# DiD / staged rollout (auto-detected from pre/post treated fields)
PYTHONPATH=. python3 -m src.cli decide --pre-control 1000 --post-control 1200 --pre-treated 200 --post-treated 280

# Experiment planning (auto-detected from --baseline + --mde)
PYTHONPATH=. python3 -m src.cli decide --baseline 0.05 --mde 10 --traffic 10000
```


**Auto-detection matrix:**
| You provide... | It runs... |
|---|---|
| `--control` + `--variant` | Frequentist A/B |
| `--control` + `--variant` + `--bayesian` | Bayesian A/B |
| `--pre-control` + `--post-control` + `--pre-treated` + `--post-treated` | DiD (Difference-in-Differences) |
| `--baseline` + `--mde` | Experiment planning |

**JSON-RPC:** `{"jsonrpc":"2.0","method":"decide","params":{...fields...},"id":"1"}` — same auto-detection over stdio or HTTP.

---

### Experiment Planning (ab_plan)

Estimate required sample size, duration, and feasibility before running an experiment:

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli plan --baseline 0.02 --mde 5 --traffic 5000
```

**Parameters:**
- `--baseline` (required): Baseline conversion rate (e.g., `0.02` for 2%)
- `--mde` (required): Minimum detectable effect as % lift (e.g., `5` for 5% lift)
- `--traffic` (required): Daily traffic per arm
- `--confidence` (default `0.95`): Confidence level
- `--power` (default `0.8`): Statistical power
- `--allocation`: `equal` (default) or `custom`
- `--allocation-ratio`: Custom ratio when allocation=custom (e.g., `0.3/0.7`)
- `--format`: `json` (default) or `text`

**Planning output:**
```json
{
  "mode": "planning",
  "recommendation": {
    "decision": "feasible|slow|not_recommended",
    "confidence": "high|medium|low",
    "summary": "..."
  },
  "planning": {
    "required_sample_per_arm": 182934,
    "total_required": 365868,
    "estimated_days": 36.6,
    "feasibility": "slow",
    "allocation_used": {"control": 0.5, "variant": 0.5}
  },
  "warnings": [...]
}
```

**Feasibility thresholds:**
- `feasible`: ≤14 days
- `slow`: 15–60 days
- `not_recommended`: >60 days

### A/B Test Analysis (Frequentist)

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli ab --control 100/5000 --variant 130/5000
```

**Parameters:**
- `--control`: Control group conversions/total (e.g., `100/5000`)
- `--variant`: Variant group conversions/total (e.g., `130/5000`)
- `--name`: Variant name (optional, default: `variant_1`)
- `--format`: Output format `json` (default) or `text`

**Sequential / Early Stopping (optional):**
- `--sequential/--no-sequential`: Enable sequential early stopping evaluation
- `--experiment-start`, `--experiment-end`: ISO 8601 timestamps for runtime calculation
- `--min-runtime-days` (default 7): Minimum days before early stop is considered
- `--min-sample-per-arm` (default 2000): Minimum sample per arm before early stop
- `--early-stop-p` (default 0.01): p-value threshold for early stop
- `--max-runtime-days`: Hard cap; escalates if exceeded without strong result

**Trigger logic:** Both min-runtime AND min-sample-per-arm must be met, AND p-value below `--early-stop-p`. Max runtime exceeded always escalates.
```bash
PYTHONPATH=. python3 -m src.cli ab --control 100/5000 --variant 130/5000
```

**Example Output:**
```json
{
  "schema_version": "0.8.0",
  "mode": "ab_test",
  "recommendation": {
    "decision": "ship",
    "confidence": "medium",
    "summary": "Variant performs 30.00% better (p=0.0454). Ship it.",
    "primary_metricLift": 30.0,
    "p_value": 0.045361
  },
  "statistics": {
    "control_rate": 0.02,
    "variant_rate": 0.026,
    "relative_lift_pct": 30.0,
    "z_score": 2.0013,
    "p_value": 0.045361,
    "lift_ci_95": [0.000124, 0.011876],
    "relative_lift_ci_95": [0.619, 59.381]
  },
  "traffic_stats": {
    "control_size": 5000,
    "variant_size": 5000,
    "total_size": 10000
  },
  "warnings": [],
  "next_steps": ["Deploy variant", "Monitor over time for regression"],
  "audit": {
    "decision_path": [
      {"step": "Input validation", "passed": true},
      {"step": "Traffic check", "passed": true},
      {"step": "Conversion rate calculation", "passed": true},
      {"step": "Statistical significance test", "passed": true},
      {"step": "Effect size check", "passed": true},
      {"step": "Decision", "passed": true}
    ]
  }
}
```

### Bayesian A/B Test

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli bayes --control 100/5000 --variant 130/5000
```

**Uses Beta-Binomial conjugate model with Jeffreys prior.**
- Prior: Beta(0.5, 0.5) — uninformative
- Posterior: Beta(α + successes, β + failures)
- Decision via Monte Carlo simulation (20k samples)
- Thresholds: P(variant wins) ≥ 0.95 → ship, ≤ 0.05 → reject

**Parameters:**
- `--control`, `--variant`: Conversions/total (same as `ab`)
- `--name`: Variant name
- `--format`: `json` (default) or `text`
- `--samples`: Monte Carlo samples (default: 20000)

**Example output:**
```json
{
  "schema_version": "0.8.0",
  "timestamp": "2026-05-06T13:00:00.000Z",
  "mode": "bayesian_ab",
  "recommendation": {
    "decision": "ship",
    "confidence": "medium",
    "summary": "Variant wins with P(better)=0.976. Median lift=30.10%. Ship.",
    "primary_metricLift": 30.10,
    "p_value": 0.9758
  },
  "statistics": {
    "control_rate_observed": 0.0200,
    "variant_rate_observed": 0.0260,
    "relative_lift_pct": 30.00,
    "posterior_control": {"alpha": 100.5, "beta": 4900.5, "mean": 0.0201},
    "posterior_variant": {"alpha": 130.5, "beta": 4870.5, "mean": 0.0261},
    "p_variant_wins": 0.9758,
    "p_control_wins": 0.0239,
    "p_tie": 0.0003,
    "lift_median_pct": 30.10,
    "lift_95ci_pct": [0.20, 69.15],
    "expected_lift_hdi_95": [0.0004, 0.0014],
    "relative_lift_hdi_95": [2.00, 70.00],
    "monte_carlo_samples": 20000,
    "prior_used": {"alpha": 0.5, "beta": 0.5, "type": "Jeffreys"}
  },
  "traffic_stats": {
    "control_size": 5000,
    "variant_size": 5000,
    "total_size": 10000
  },
  "warnings": [],
  "next_steps": ["Deploy variant", "Monitor for regression"],
  "audit": {
    "experiment_type": "bayesian_ab",
    "thresholds_applied": {"ship": 0.95, "reject": 0.05},
    "assumptions": ["Independent observations between groups", "No selection bias in group assignment", "Jeffrey's prior is appropriate for conversion rates"],
    "limitations": ["Monte Carlo simulation has finite sampling error", "No multiple testing correction applied"]
  },
  "inputs": {
    "control_conversions": 100,
    "control_total": 5000,
    "variant_conversions": 130,
    "variant_total": 5000
  }
}
```

Access fields via `.` attribute (e.g. `result.recommendation.decision`) or `.model_dump()` for dict. Serialize with `.model_dump_json()`.

**When to use Bayesian vs Frequentist:**

### DiD Analysis

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli did --pre-control 1000 --post-control 1100 --pre-treated 900 --post-treated 1150
```

**Parameters:**
- `--pre-control`: Control group metric before treatment
- `--post-control`: Control group metric after treatment
- `--pre-treated`: Treated group metric before treatment
- `--post-treated`: Treated group metric after treatment
- `--n-bootstrap` (default 2000, range 500–10000): Number of bootstrap resamples for DiD CI

### Cohort / Segment Breakdown

When an aggregate A/B or DiD result is inconclusive, break down results by user segment to find hidden signals:

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli cohort-breakdown --file segments.json
```

**Input format (JSON):**
```json
{
  "experiment_id": "checkout-v3",
  "metric": "conversion_rate",
  "prior_result_id": "dec_20260501_001",
  "prior_decision": "wait",
  "segments": [
    {
      "segment_name": "new_users",
      "segment_definition_note": "Users registered within last 30 days",
      "control_conversions": 21,
      "control_total": 1000,
      "variant_conversions": 67,
      "variant_total": 1000
    },
    {
      "segment_name": "returning_users",
      "segment_definition_note": "Users registered more than 30 days ago",
      "control_conversions": 220,
      "control_total": 4000,
      "variant_conversions": 228,
      "variant_total": 4000
    }
  ]
}
```

**Input format (CSV alternative):**
```
segment_name,segment_definition_note,arm,conversions,total
new_users,Users registered within last 30 days,control,21,1000
new_users,Users registered within last 30 days,variant,67,1000
returning_users,Users registered more than 30 days ago,control,220,4000
returning_users,Users registered more than 30 days ago,variant,228,4000
```

**Parameters:**
- `--file`: Path to JSON or CSV segment file
- `--json`: JSON input string (alternative to `--file`)
- `--format`: Output format `json` (default) or `text`
- `--save`: Save result to experiment history

**Multiple comparison correction:**
- 4+ segments: Benjamini-Hochberg FDR correction applied automatically
- 5+ segments: Also offers Bonferroni as alternative via `--method bonferroni`

**Example output:**
```json
{
  "method": "experiment_cohort_breakdown",
  "cohort_decision_override": true,
  "cohort_override_reason": "Strong positive signal in 'new_users' (lift=219.0%, adj-p=0.0000) contradicts aggregate decision 'wait'",
  "interaction_flag": false,
  "segments": [
    {
      "segment_name": "new_users",
      "control_rate": 0.021,
      "variant_rate": 0.067,
      "relative_lift_pct": 219.05,
      "p_value_raw": 0.0000,
      "p_value_adjusted": 0.0000,
      "decision": "strongly_positive",
      "priority_rank": 1
    }
  ],
  "priority_ranking": [
    {"rank": 1, "segment": "new_users", "rationale": "Strong positive effect (lift=219.1%, adj-p=0.0000). Highest priority."}
  ],
  "summary": "new_users drives the effect. 1 segment(s) positive.",
  "recommended_next_action": "targeted_rollout"
}
```

**When to use cohort breakdown:**
- Aggregate A/B result is `keep_running` or `escalate` — segment analysis may reveal a hidden signal
- One segment is strongly positive while another is strongly negative (interaction flag)
- You want to ship only to specific segments rather than all users

**Key features:**
- Per-segment two-proportion z-test with 95% confidence
- Benjamini-Hochberg FDR correction for 4+ segments (controls false-discovery rate)
- Priority ranking by absolute lift magnitude
- Cohort decision override: fires when a segment contradicts the aggregate decision
- Interaction flag: triggered when segments show opposing strongly-significant directions

### Decision Audit

Reconstruct and explain a previous decision:

```bash
# Save result to file
PYTHONPATH=. python3 -m src.cli ab --control 100/5000 --variant 130/5000 > /tmp/result.json

# Audit it (human-readable)
PYTHONPATH=. python3 -m src.cli audit /tmp/result.json --format text

# Audit with experiment maturity assessment
PYTHONPATH=. python3 -m src.cli audit /tmp/result.json --maturity
```

**Maturity assessment** (with `--maturity` flag):
- Scores experiments 0–100 across 8 checks
- Labels: `mature` (≥90), `adequate` (≥70), `immature` (≥50), `inadequate` (<50)
- Checks: decision path completeness, critical warnings, limitations documented, traffic sufficiency, confidence level, step documentation

**Example audit output:**
```
-- DECISION PATH --
1. Input validation [✓]
   control_total: 5000, variant_total: 5000
2. Traffic check [✓]
   control_size: 5000, min_required: 1000
3. Conversion rate calculation [✓]
   control_rate: 0.02, variant_rate: 0.026
4. Statistical significance test [✓]
   p_value: 0.045361, alpha: 0.05
5. Effect size check [✓]
   lift_pct: 30.0, threshold: 1
6. Decision [✓]
   decision: ship, confidence: medium

-- FINAL DECISION --
  Decision: SHIP
```

### Experiment History & Persistence

All commands support `--save` to persist results to local SQLite history:

```bash
# Run and save in one step
PYTHONPATH=. python3 -m src.cli ab --control 100/5000 --variant 130/5000 --save
PYTHONPATH=. python3 -m src.cli did --pre-control 1000 --post-control 1100 --pre-treated 900 --post-treated 1150 --save
PYTHONPATH=. python3 -m src.cli plan --baseline 0.02 --mde 5 --traffic 5000 --save
```

**History commands:**

```bash
# List recent experiments
PYTHONPATH=. python3 -m src.cli history
PYTHONPATH=. python3 -m src.cli history --mode ab_test --limit 10

# Compare multiple experiments by ID
PYTHONPATH=. python3 -m src.cli compare 1 2 3

# Save a prior JSON result file to history
PYTHONPATH=. python3 -m src.cli save /tmp/result.json --name "checkout-v3-test"
```

**History output example:**
```
ID    Date       Mode       Decision   Lift     P-value  Summary
--------------------------------------------------------------------
3     2026-04-30 did        ship       16.67    -        Treatment effect is 150.00...
2     2026-04-30 ab_test    escalate   6.25     0.6947   Results not conclusive...
1     2026-04-30 ab_test    ship       30.00    0.0454   Variant performs 30.00%...
```

**Compare output example:**
```
EXPERIMENT COMPARISON
==================================================
Experiments compared: 3

Summary by decision:
  SHIP: 2 experiment(s)
  ESCALATE: 1 experiment(s)

Summary by mode:
  ab_test: 2 experiment(s)
  did: 1 experiment(s)

Lift summary: max=30.00%, min=6.25%, avg=17.64% (3 experiments)

Attention needed: 2 experiments recommend ship. Review if they test the same metric.
```

**Persistence:**
- SQLite DB stored at `~/.agent-causal/history.db`
- All experiment modes supported: `ab_test`, `did`, `planning`
- Full raw JSON preserved for audit reconstruction
- Filter by mode, limit results, name experiments for later reference

## Decision Reference

| Decision | Meaning | When |
|----------|---------|------|
| `ship` | Deploy variant | p < 0.05 AND positive lift |
| `keep_running` | Continue experiment | p < 0.3, trending positive |
| `reject` | Do not deploy | p < 0.05 AND negative lift |
| `escalate` | Needs human review | Not conclusive or critical warnings |
| `targeted_rollout` | Ship to specific segment only | Strong signal in one segment, aggregate inconclusive |
| `full_rollout` | Ship to all users | All segments positive |
| `abandon_segment` | Do not ship to specific segment | Strong negative in one segment despite aggregate ship |
| `confirm_rejection` | Confirm abandonment | All segments negative |

## Python API

```python
import sys
sys.path.insert(0, '~/clawd/agent-causal-decision-tool')

from src.ab_test import calculate_ab

result = calculate_ab({
    "control_conversions": 100,
    "control_total": 5000,
    "variant_conversions": 130,
    "variant_total": 5000
})

if result.recommendation.decision == "ship":
    # Deploy variant
    pass
```

## Warnings & Limitations

- **LOW_TRAFFIC**: Sample size below 1000 per group
- **SMALL_EFFECT**: Lift < 1%, may not be practically significant
- **INCONCLUSIVE**: Result not statistically significant or strong enough to act on
- **NOT_SIGNIFICANT**: Far from significant; consider stopping the experiment
- **BORDERLINE_P_VALUE**: p-value between 0.05 and 0.10 — weak evidence, not conclusive
- **CORRECTION_CONSERVATIVE**: Multiple comparison correction applied; may increase false negatives
- **SEQUENTIAL_EARLY_STOP**: Experiment stopped early via sequential testing; interpret with caution
- **SEQUENTIAL_CONDITIONS_NOT_MET**: Early stopping conditions not met; normal decision applied
- **MAX_RUNTIME_EXCEEDED**: Hard runtime cap exceeded without strong result; escalating
- **ZERO_BASELINE**: Pre-period values cannot be zero for reliable DiD
- **PARALLEL_TRENDS_VIOLATED**: Control and treated groups show very different pre-to-post ratios (critical)
- **PARALLEL_TRENDS_WEAK**: Ratios diverge somewhat; monitor closely
- **BOTH_GROUPS_GREW**: Both groups grew; cannot separate treatment effect from time trend
- **AGGREGATE_DATA**: Analysis on aggregated data; use individual-level data for robust inference
- **AGGREGATE_DATA_DID**: DiD result with high caution; not equivalent to a randomized experiment
- **SINGLE_PRE_PERIOD**: Only one pre-period observation; parallel trends cannot be assessed
- **SMALL_SAMPLE**: Sample size small; estimates unreliable
- **IMBALANCED_GROUPS**: Treatment/control group sizes very different; may bias DiD estimate
- **LARGE_EFFECT_SMALL_SAMPLE**: Large effect estimate from small sample; prioritize replication
- **PARALLEL_TRENDS_NO_DATA**: No pre-period count provided; parallel trends cannot be assessed
- **BOOTSTRAP_CI_UNRELIABLE**: Bootstrap CI not computed — count < 100 or zero baseline
- **BOOTSTRAP_CI_WIDE**: Bootstrap CI range > 2×|DiD estimate|; point estimate uncertain
- **DID_CI_CROSSES_ZERO**: Bootstrap CI crosses zero; effect direction uncertain
- **SLOW_EXPERIMENT**: Estimated duration > 30 days; seasonal effects may confound results
- **INFEASIBLE_EXPERIMENT**: Duration too long; consider DiD instead
- **SMALL_MDE**: MDE very small; may require impossibly large sample
- **BASELINE_VERY_LOW**: Baseline rate < 0.5%; estimations may be unreliable
- **BASELINE_NEAR_ZERO**: Baseline rate < 0.1%; do not run experiment without careful review
- **PRIOR_DOMINATES**: Very low total traffic; Jeffreys prior dominates posterior; interpret with caution
- **CREDIBLE_INTERVAL_WIDE**: Bayesian credible interval is very wide; estimate uncertain

## Schema Contract

The tool exposes a versioned schema contract for agent consumption:

```bash
cd ~/clawd/agent-causal-decision-tool
PYTHONPATH=. python3 -m src.cli schema
```

This prints `schema.json` — a wrapper containing `schema_version`, `schema_coverage` (`ab`, `did`, `plan`, `bayes`), `schema_coverage_pending` (`cohort`), `severity_contract`, and `definitions` (JSON Schema from Pydantic models).

All output models include `schema_version` field injected from package metadata — never hardcoded.

## Location

- **GitHub:** https://github.com/ZhuMorris/agent-causal-decision-tool
- **Local:** `~/clawd/agent-causal-decision-tool/`

## Dependencies

- Python 3.9+
- click >= 8.1.0
- scipy >= 1.11.0
- numpy >= 1.26.0
- pydantic >= 2.10.0

## External Connectors

Fetch experiment data directly from external sources. The `connect` action normalizes external data into the internal experiment schema before running a decision.

### PostHog

```bash
# Health check (validates credentials, no data fetched)
PYTHONPATH=. python3 -m src.cli connect posthog --dry-run

# Fetch experiment and print normalized data
PYTHONPATH=. python3 -m src.cli connect posthog --experiment-id <id>

# Fetch and run through decision workflow automatically
PYTHONPATH=. python3 -m src.cli connect posthog --experiment-id <id> --decide

# JSON-RPC call
{"jsonrpc":"2.0","method":"connect","params":{"source":"posthog","experiment_id":"<id>"},"id":"1"}
```

**Environment / config:**
- `POSTHOG_API_KEY` + `POSTHOG_PROJECT_ID` env vars, OR
- `~/.posthogrc` with `api_key`, `project_id`, `instance_url` fields

**Connector result schema:**
```json
{
  "data": { "control_conversions": 120, "control_total": 5000, "variant_conversions": 145, "variant_total": 5000 },
  "source_metadata": { "connector": "posthog", "experiment_id": "...", "fetch_timestamp": "..." },
  "warnings": []
}
```

**Errors:**
- `INSUFFICIENT_DATA` — experiment found but missing required fields
- `ConnectorAuthError` — invalid/missing API key
- `ConnectorNotFoundError` — experiment not found
