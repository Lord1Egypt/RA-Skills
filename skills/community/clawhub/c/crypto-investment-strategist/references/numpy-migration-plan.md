# Numpy Migration Plan

## Goal

Restore a numpy-based indicator pipeline after the runtime environment can install and execute numpy reliably.

The current pure Python implementation is a compatibility fallback. Keep it as the known-good baseline until the numpy path is fully validated.

## Scope

Review and update these scripts:

- `scripts/calculate_indicators.py`
- `scripts/auto_rank_assets.py`
- `scripts/run_investment_workflow.py`

Check whether any helper logic inside other scripts should also be aligned with the restored indicator outputs.

## Migration Principles

1. Preserve current CLI interfaces unless there is a strong reason to change them.
2. Preserve JSON output schema unless an improvement is clearly justified.
3. Keep the pure Python version available until numpy regression checks pass.
4. Prefer a small compatibility layer over scattered conditional logic.
5. Validate numerical consistency before optimizing for speed.

## Recommended Implementation Strategy

### Option A. Safe dual-path rollout

Use a runtime switch or internal adapter so both implementations can exist temporarily.

Suggested pattern:

- Extract shared indicator interface into a small internal module or function boundary.
- Implement a `pure_python` backend.
- Implement a `numpy` backend.
- Default to `numpy` only after validation is complete.

This is the safest path because it supports side-by-side comparison during migration.

### Option B. Direct replacement

Replace the current implementation directly.

Use this only if:

- the code remains easy to audit
- the formulas are already well covered by regression samples
- rollback is trivial

## Environment Readiness Checklist

Do not begin the migration until all items below are true:

- `python3` is available
- `pip` or another package installation path is available
- `numpy` can be installed successfully in the target runtime
- the installed numpy version is recorded
- the runtime can execute all existing scripts without import path issues

Suggested verification commands:

```bash
python3 -c "import sys; print(sys.version)"
python3 -c "import numpy; print(numpy.__version__)"
```

## Step-by-Step Plan

### Step 1. Freeze the current baseline

Before changing code:

- save representative outputs from the pure Python implementation
- cover at least BTC, ETH, and one higher-volatility altcoin such as SOL
- keep samples for multiple timeframes if supported by the current flow

Capture outputs for:

- `calculate_indicators.py`
- `auto_rank_assets.py`
- `run_investment_workflow.py`

### Step 2. Identify indicator formulas that must match

Review the current implementation and list every computed field that affects downstream decisions.

At minimum verify the exact behavior for:

- moving averages
- RSI
- MACD
- ATR
- any trend classification fields
- any derived booleans such as `above_ma20` and `above_ma50`

Document rounding rules and handling for short histories or missing values.

### Step 3. Introduce the numpy implementation

Rebuild the indicator calculations with numpy arrays.

Guidelines:

- keep formulas explicit and readable
- avoid premature vectorization tricks that make audits hard
- guard against length mismatches and NaN propagation
- use the same output keys as the current implementation

### Step 4. Run side-by-side comparisons

Compare pure Python and numpy outputs on the same saved input files.

Acceptable outcome:

- categorical fields match exactly
- numerical fields are equal or within a small documented tolerance
- ranking order is unchanged unless the formula correction is intentional

If ranking changes, record whether the change is a bug fix or a regression.

### Step 5. Validate the full workflow

Re-run:

```bash
python3 scripts/auto_rank_assets.py --symbols BTC ETH SOL
python3 scripts/run_investment_workflow.py --symbols BTC ETH SOL --capital 10000 --risk medium --regime uptrend
```

Also re-run:

```bash
python3 scripts/allocate_portfolio.py --capital 10000 --risk medium --regime uptrend
```

The allocation script does not depend on numpy indicators directly, but re-running it confirms the end-to-end workflow still feels consistent after the migration.

### Step 6. Decide the final fallback policy

Choose one of these final states:

- **Preferred:** keep both backends, default to numpy, and fall back gracefully if numpy is unavailable
- **Strict:** require numpy and remove the pure Python path

Preferred is better for portability.

## Regression Checklist

Mark the migration complete only when all checks pass:

- indicator script runs without import errors
- output schema remains stable
- BTC sample output matches expected values within tolerance
- ETH sample output matches expected values within tolerance
- SOL sample output matches expected values within tolerance
- asset ranking still produces sensible ordering
- workflow script completes successfully
- snapshot logging still works when used with migrated outputs
- README and SKILL instructions reflect the final runtime requirement

## Recommended Test Fixtures

Create or preserve a small fixture set with:

- one trending market sample
- one range market sample
- one more volatile market sample

Keep fixtures in JSON so they can be reused for future refactors.

## Risks to Watch

### Numerical drift

Small formula or initialization differences can change RSI, MACD, or ATR enough to alter ranking.

### NaN handling

Vectorized code can silently propagate NaN values. Check warm-up periods carefully.

### Hidden schema drift

Even if calculations are correct, renamed keys or changed null behavior can break downstream scripts.

### Over-optimization

A fast implementation is not useful if future maintainers cannot verify the formula logic quickly.

## Completion Definition

The numpy migration is complete only when:

1. numpy is available in the runtime
2. indicator outputs are validated against the current baseline
3. downstream ranking and workflow outputs are rechecked
4. runtime requirements are documented clearly
5. the final backend policy is chosen and implemented

## Follow-up Files to Update After Migration

Update these files after the actual switch is done:

- `README.md`
- `SKILL.md`
- any script help text that mentions the pure Python fallback

If the migration changes behavior materially, add a short changelog note in the repository history or release notes.
