---
name: "fp-dcf"
description: "Estimate intrinsic value with a first-principles DCF from structured JSON or provider-backed ticker input, and return auditable FCFF, WACC, and per-share value output."
metadata: {"openclaw":{"emoji":"📉","homepage":"https://github.com/tiejiang8/FP-DCF","requires":{"anyBins":["python3","python"]}}}
user-invocable: true
---

# FP-DCF

Version: `v0.6.0`

## Repository Workflow Notice

- For this repository, GitHub submissions do not use a separate branch workflow.
- Do not create a feature branch for routine updates; commit and publish on the designated branch directly unless the user explicitly asks for a different flow.
- If a default workflow suggests opening a branch or PR, treat that as incorrect for this repository.

Use this skill when the task is to estimate intrinsic value from structured fundamentals and assumption inputs using a disciplined, auditable DCF workflow.

## Invocation Scope

Use this skill when the user asks for:

- intrinsic value
- DCF valuation
- `FCFF` / `WACC` based valuation
- market-implied growth
- what growth rate is implied by the current market price
- `WACC / terminal-growth` sensitivity
- auditable valuation JSON for a company

Do not use this skill as the only answer when the user asks:

- should I buy or sell this stock
- which stock is better
- build me a portfolio
- rank an industry
- backtest a strategy
- analyze a bank, insurer, broker, or financial-sector company

For investment-report tasks, FP-DCF may be used only as the valuation layer. The agent must still handle:

- industry structure
- competitive advantage
- business quality
- revenue / margin drivers
- balance-sheet risk
- management and capital allocation
- valuation conclusion

## Model Selection Rule

- Use `steady_state_single_stage` when the company is mature, normalized, or the user wants a conservative base case.
- Use `two_stage` when there is a defensible explicit high-growth period followed by stable growth.
- Use `three_stage` when high growth is expected to fade gradually before terminal growth.
- Use `market_implied_growth.enabled=true` when the user asks what the current price implies.
- Use sensitivity output by default unless the environment lacks `matplotlib` or the user asks for JSON-only output.

## Runtime Contract

This repository is executable when installed as a skill because it includes a concrete CLI entrypoint:

- Primary runner: `{baseDir}/scripts/run_dcf.py`
- Python module entrypoint: `python3 -m fp_dcf.cli`
- Sample input: `{baseDir}/examples/sample_input.json`
- Base Python dependencies for the default one-click path: `akshare`, `baostock`, `numpy`, `pandas`, `yfinance`, `matplotlib`

Preferred execution pattern:

1. Build a JSON payload that matches `{baseDir}/examples/sample_input.json`.
2. Write that payload to a temporary JSON file in the workspace.
3. Run one of:
   - `python3 {baseDir}/scripts/run_dcf.py --input /path/to/input.json --pretty`
   - `python {baseDir}/scripts/run_dcf.py --input /path/to/input.json --pretty`
4. Read the JSON output and present the result to the user.

If the runtime supports stdin piping, this also works:

```bash
python3 {baseDir}/scripts/run_dcf.py --pretty < /path/to/input.json
```

Provider-backed normalization uses a local provider cache by default. To force a fresh pull for the current request, run:

```bash
python3 {baseDir}/scripts/run_dcf.py --input /path/to/input.json --pretty --refresh-provider
```

If the runtime needs an isolated cache location, pass:

```bash
python3 {baseDir}/scripts/run_dcf.py --input /path/to/input.json --pretty --cache-dir /path/to/cache
```

The main runner already returns a compact sensitivity summary and auto-renders both SVG and PNG chart artifacts by default. If the user explicitly asks for a `WACC x Terminal Growth` chart or sensitivity table, keep using the same main runner so the valuation JSON and artifact paths come back in a single output:

```bash
python3 {baseDir}/scripts/run_dcf.py \
  --input /path/to/input.json \
  --output /path/to/output.json \
  --pretty
```

That one command will default the chart artifact paths to `/path/to/output.sensitivity.svg` and `/path/to/output.sensitivity.png`.

## Input Shape

The expected JSON object contains:

- `ticker`
- `market`
- `valuation_model`
- `assumptions`
- `fundamentals`

Minimum required values for a useful result:

- `assumptions.effective_tax_rate`
- `assumptions.marginal_tax_rate`
- `assumptions.risk_free_rate`
- `assumptions.equity_risk_premium`
- `assumptions.beta`
- `assumptions.pre_tax_cost_of_debt`
- `fundamentals.fcff_anchor` or `fundamentals.ebit`

Supported `valuation_model` values in `v0.6.0`:

- `steady_state_single_stage`
- `two_stage`
- `three_stage`

For `two_stage`, the engine continues to support the legacy `assumptions.high_growth_rate` / `high_growth_years` fields and also accepts `assumptions.stage1_growth_rate` / `stage1_years` as compatible aliases.

For `three_stage`, the valuation path requires these assumption fields:

- `assumptions.terminal_growth_rate`
- `assumptions.stage1_growth_rate`
- `assumptions.stage1_years`
- `assumptions.stage2_end_growth_rate`
- `assumptions.stage2_years`

For `three_stage`, this optional field is also supported:

- `assumptions.stage2_decay_mode` with default `linear`

`market_implied_growth` is the only formal market-implied block. Its meaning depends on `valuation_model`: `steady_state_single_stage` solves market-implied long-term growth, while `two_stage` and `three_stage` solve market-implied stage-1 growth.

If `fundamentals.fcff_anchor` is not supplied, the runner computes it from:

- `ebit`
- `da`
- `capex`
- `delta_nwc` or a fallback working-capital field

If those structured fields are mostly missing, the runner can auto-normalize them from a live provider when:

- `provider` is set to `yahoo`, or
- `provider` is set to `akshare_baostock` for `market=CN`, or
- the payload has a `ticker` but is missing core DCF inputs

The minimal provider-backed input shape is:

```json
{
  "ticker": "AAPL",
  "market": "US",
  "provider": "yahoo",
  "statement_frequency": "A",
  "valuation_model": "steady_state_single_stage",
  "assumptions": {
    "terminal_growth_rate": 0.03
  }
}
```

For China A-shares, this explicit provider shape is also supported:

```json
{
  "ticker": "600519.SH",
  "market": "CN",
  "provider": "akshare_baostock",
  "statement_frequency": "A",
  "valuation_model": "steady_state_single_stage",
  "assumptions": {
    "terminal_growth_rate": 0.025
  }
}
```

When `market="CN"` and Yahoo normalization fails, FP-DCF automatically falls back to `akshare_baostock`. In that path, AkShare provides statement data and BaoStock provides price history and the latest close.

The payload can also drive normalization behavior through an optional `normalization` object:

- `normalization.provider`
- `normalization.use_cache`
- `normalization.refresh`
- `normalization.cache_dir`
- `normalization.max_cache_age_hours`

The payload can also request sensitivity analysis through an optional `sensitivity` object:

- `sensitivity.enabled`
- `sensitivity.metric`
- `sensitivity.detail`
- `sensitivity.chart_path`
- `sensitivity.wacc_range_bps`
- `sensitivity.wacc_step_bps`
- `sensitivity.growth_range_bps`
- `sensitivity.growth_step_bps`

The payload can also request market-implied growth through an optional `market_implied_growth` object:

- `market_implied_growth.enabled`
- `market_implied_growth.lower_bound`
- `market_implied_growth.upper_bound`
- `market_implied_growth.solver`
- `market_implied_growth.tolerance`
- `market_implied_growth.max_iterations`

`market_implied_growth` always solves one field based on `valuation_model`:

- `steady_state_single_stage` -> `growth_rate`
- `two_stage` -> `stage1_growth_rate`
- `three_stage` -> `stage1_growth_rate`

Sensitivity output is enabled by default. To disable it for a specific run:

- pass `--no-sensitivity`, or
- set `sensitivity.enabled=false`

Live provider-backed runs are inherently date-sensitive. Do not hard-code expected valuation numbers when validating this path; validate the presence and plausibility of the returned fields instead.

Provider-backed runs return `data_freshness`:

- `fresh`: provider cache age is within the allowed window
- `stale`: provider cache age exceeds the allowed window; treat the valuation as degraded
- `unknown`: cache creation time is missing or unreadable; treat the valuation as degraded
- `missing`: provider data is structurally missing; treat the valuation as degraded or fail if a required field is unavailable
- `user_supplied`: manual structured input; do not force a freshness judgment

Default freshness windows are `24` hours for price-sensitive provider snapshots and `168` hours for statement-only snapshots. Use `--refresh-provider`, `normalization.refresh=true`, or a stricter `normalization.max_cache_age_hours` when the user asks for current market data.

## Core Rules

### Tax Policy

- Keep the operating tax estimate for `FCFF` separate from the marginal tax assumption used in `WACC`.
- If the statement-level tax rate is available, prefer it for `EBIAT/NOPAT`.
- If the marginal tax rate is manual or market-defaulted, expose that source in the output.
- Do not silently reuse one tax rate for both paths when the intended sources differ. If a fallback reuse happens, surface it in `warnings`.

### Working-Capital Policy

Use this fallback order and report which path was used:

1. `delta_nwc`
2. `op_nwc_delta`
3. `nwc_delta`
4. cash-flow working-capital change fields such as `change_in_working_capital`

If all paths fail, flag the result as degraded rather than pretending the estimate is fully reliable.

### FCFF Policy

- Prefer a normalized steady-state `FCFF` anchor for single-stage valuation.
- Prefer `NOPAT + ROIC + reinvestment` when the driver data is usable.
- Fall back to normalized historical `FCFF` only when the operating-driver path is incomplete.
- Do not discount historical realized `FCFF` as if it were a forward forecast.

### WACC Policy

- Use explicit sources for risk-free rate, ERP, beta, pre-tax debt cost, and capital weights.
- Prefer explicit capital weights from the input payload when available.
- Apply the marginal tax assumption only to the debt tax shield.
- Attach a warning when key inputs are manual, defaulted, stale, or missing.

### Sector Policy

- Financial institutions often produce unreliable `FCFF` under industrial-company DCF logic.
- When the company is bank-like, insurer-like, broker-like, or otherwise balance-sheet-driven, downgrade or exclude the result unless the workflow explicitly supports that sector.

## Output Requirements

Always return:

- valuation model used
- `contract_version`
- `requested_valuation_model`
- `effective_valuation_model`
- `degraded`
- major assumptions with source labels
- `FCFF` anchor and anchor method
- working-capital source used
- `WACC` inputs and capital weights
- enterprise value, equity value, and per-share value when available
- `valuation.present_value_stage1`
- `valuation.present_value_stage2`
- `valuation.present_value_terminal`
- `valuation.terminal_value`
- `valuation.terminal_value_share`
- `valuation.explicit_forecast_years`
- `market_implied_growth` when that block is enabled and valid
- `data_freshness` with `provider`, `snapshot_as_of`, `cache_created_at`, `cache_age_hours`, `freshness_class`, and `requires_refresh`
- provider cache status diagnostics when provider-backed normalization is used
- diagnostics, warnings, and degradation flags
- by default, return a compact sensitivity summary plus both chart file paths

Canonical JSON Schema contracts live in:

- `contracts/valuation_input.schema.json`
- `contracts/valuation_output.schema.json`
- `contracts/data_freshness.schema.json`
- `contracts/market_implied_growth.schema.json`
- `contracts/sensitivity_summary.schema.json`

Treat `contracts/` as machine contracts, not as loose documentation.

`contract_version` exists so downstream agents and pipelines can make explicit compatibility decisions.

Schema-valid does not guarantee business-semantic equivalence. Differences in assumptions, defaults, freshness, and degraded execution paths can still materially change how the output should be interpreted.

## Execution Notes

- Use `{baseDir}` instead of guessing the install path.
- Prefer writing a JSON file and passing `--input` over hand-building one-line shell JSON.
- If the payload only contains `ticker/market` plus light assumptions, rely on provider-backed normalization instead of fabricating fundamentals.
- Use the default provider cache for repeated runs on the same ticker unless the user explicitly asks for fresh data.
- If the user asks for the latest market or statement snapshot, add `--refresh-provider` or set `normalization.refresh=true`.
- If `data_freshness.freshness_class` is `stale`, `unknown`, or `missing`, surface the warning and avoid presenting the valuation as current.
- If `data_freshness.requires_refresh=true` and the user asked for current market conditions, rerun with `--refresh-provider`.
- If the user asks for a valuation sensitivity table or heatmap, prefer the main runner with its default sensitivity output and auto-generated chart path over a separate second command.
- If the caller needs the full numeric heatmap grid in JSON, set `sensitivity.detail=true` instead of bloating the default output for every run.
- Only use `--sensitivity-chart-output` or `sensitivity.chart_path` when the caller explicitly wants to override the default artifact location.
- The default one-click path assumes `matplotlib` is installed, because PNG/SVG chart artifacts are rendered automatically.
- If the environment intentionally excludes `matplotlib`, disable sensitivity first with `--no-sensitivity` or `sensitivity.enabled=false` before running the main CLI.
- If `per_share_value` sensitivity is unavailable because `shares_out` is missing, try `--refresh-provider` first or switch the sensitivity metric to `equity_value`.
- If the user only gives high-level valuation preferences, ask for or derive the missing structured inputs before running the script.
- If `valuation_model=three_stage` is missing `stage1_growth_rate`, `stage1_years`, `stage2_end_growth_rate`, `stage2_years`, or `terminal_growth_rate`, fail with a clear error instead of falling back.
- If `valuation_model` is unknown, fail with an error containing `unsupported valuation_model`; do not silently remap it to another model.
- Do not silently degrade a requested `three_stage` valuation into `two_stage` or `steady_state_single_stage`.
- Keep the market-implied growth contract stable in `v0.6.0`: `market_implied_growth` remains the only formal market-implied block.
- Keep `market_implied_growth` as the only formal market-implied block and derive the solved field from `valuation_model`.
- Reject legacy market-implied inputs with explicit errors.
- If the user wants single-stage market-implied growth, route that request through `payload.market_implied_growth.enabled=true` and let `valuation_model=steady_state_single_stage` determine the solved field.
- Read [references/methodology.md](./references/methodology.md) only when you need policy detail beyond this file.

## Reference Map

Read only what you need:

- [references/methodology.md](./references/methodology.md) for the valuation methodology
- [examples/sample_input.json](./examples/sample_input.json) for the intended input contract
- [examples/sample_output.json](./examples/sample_output.json) for the intended output contract
- [examples/sample_input_market_implied_growth_single_stage.json](./examples/sample_input_market_implied_growth_single_stage.json) for a minimal single-stage market-implied growth example
- [examples/sample_input_market_implied_growth_two_stage.json](./examples/sample_input_market_implied_growth_two_stage.json) for a minimal two-stage market-implied growth example
- [examples/sample_input_market_implied_growth_three_stage.json](./examples/sample_input_market_implied_growth_three_stage.json) for a minimal three-stage market-implied growth example
- [examples/300347.sz_market_implied_growth_single_stage.json](./examples/300347.sz_market_implied_growth_single_stage.json) and [examples/300347.sz_market_implied_growth_single_stage.output.json](./examples/300347.sz_market_implied_growth_single_stage.output.json) for a real 300347.SZ single-stage market-implied demo
- [examples/300347.sz_market_implied_growth_two_stage.json](./examples/300347.sz_market_implied_growth_two_stage.json) and [examples/300347.sz_market_implied_growth_two_stage.output.json](./examples/300347.sz_market_implied_growth_two_stage.output.json) for a real 300347.SZ two-stage market-implied demo
- [examples/300347.sz_market_implied_growth_three_stage.json](./examples/300347.sz_market_implied_growth_three_stage.json) and [examples/300347.sz_market_implied_growth_three_stage.output.json](./examples/300347.sz_market_implied_growth_three_stage.output.json) for a real 300347.SZ three-stage market-implied demo
- [examples/cn_moutai_single_stage.json](./examples/cn_moutai_single_stage.json) for a CN provider-backed single-stage example
- `contracts/valuation_input.schema.json` and `contracts/valuation_output.schema.json` for the canonical JSON contracts

## Quality Bar

- Prefer explicit assumptions over hidden heuristics.
- Prefer auditable fallbacks over brittle elegance.
- Label degraded results clearly.
- Be conservative when provider data is incomplete or inconsistent.
- If a result depends heavily on terminal value, include that in the diagnostics.
