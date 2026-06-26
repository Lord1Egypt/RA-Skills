---
name: fund_buying_decision
description: Parameterize and apply a Chinese mutual-fund buy, add, reduce, or hold strategy driven by price drawdown, recurring DCA, cash-pool management, and position limits. Use when Codex needs to maintain the strategy thresholds in SKILL.md, explain or simulate a daily decision, update the bundled Eastmoney-to-SQLite importer, or produce a detailed report for a fund such as 011598.
---

# Fund Buying Decision

## Overview

Use this skill to keep a reusable fund trading framework in one place.
Prefer changing the parameter block below instead of rewriting numeric rules in prose.

Return one explicit action per decision cycle:

- `buy_dca`
- `buy_dip`
- `sell_take_profit`
- `hold`
- `skip_data_missing`

If multiple actions trigger on the same day, prefer the risk-reducing action and keep the one-trade-per-day rule.

## Strategy Parameters

Edit `editable` first. Keep `fixed` stable unless the strategy shape really changes.

```yaml
strategy_parameters:
  editable:
    capital:
      initial_cash: 1000
      weekly_dca_amount: 100
      monthly_cash_pool_inflow: 1000

    scheduling:
      weekly_pretrade_reminder:
        weekday: monday
        time_local: "09:00"
      weekly_dca:
        weekday: tuesday
      weekly_trade_reminder:
        weekday: tuesday
        time_local: "09:30"
      monthly_cash_inflow:
        schedule_type: second_to_last_business_day
        day_of_month: null
      monthly_cash_inflow_reminder:
        schedule_type: second_to_last_business_day
        day_of_month: null
        time_local: "10:00"

    price_state:
      dip_thresholds_pct: [5, 10, 15]
      dip_base_buy_amounts: [100, 150, 200]

    take_profit:
      profit_thresholds_pct: [10, 20]
      profit_sell_ratios_pct: [10, 20]

    risk:
      max_position_ratio_pct: 80
      min_position_ratio_pct: 20

  fixed:
    universe:
      allowed_fund_types:
        - index_fund
        - equity_fund
      disallowed_fund_types:
        - bond_fund
        - money_market_fund

    capital:
      fee_rate_source: fund_current_rate

    scheduling:
      trade_cutoff_local_time: "15:00"
      backtest_execution_mode: next_trading_day
      max_trades_per_day: 1

    price_state:
      recent_high_lookback_trading_days: 20
      min_trading_days_between_adds: 5
```

## Parameter Groups

Use these two buckets when maintaining the strategy:

- `editable`
  `capital.initial_cash`
  `capital.weekly_dca_amount`
  `capital.monthly_cash_pool_inflow`
  `scheduling.weekly_pretrade_reminder.weekday`
  `scheduling.weekly_pretrade_reminder.time_local`
  `scheduling.weekly_dca.weekday`
  `scheduling.weekly_trade_reminder.weekday`
  `scheduling.weekly_trade_reminder.time_local`
  `scheduling.monthly_cash_inflow.schedule_type`
  `scheduling.monthly_cash_inflow.day_of_month`
  `scheduling.monthly_cash_inflow_reminder.schedule_type`
  `scheduling.monthly_cash_inflow_reminder.day_of_month`
  `scheduling.monthly_cash_inflow_reminder.time_local`
  `price_state.dip_thresholds_pct`
  `price_state.dip_base_buy_amounts`
  `take_profit.profit_thresholds_pct`
  `take_profit.profit_sell_ratios_pct`
  `risk.max_position_ratio_pct`
  `risk.min_position_ratio_pct`

- `fixed`
  `universe.allowed_fund_types`
  `universe.disallowed_fund_types`
  `capital.fee_rate_source`
  `scheduling.trade_cutoff_local_time`
  `scheduling.backtest_execution_mode`
  `scheduling.max_trades_per_day`
  `price_state.recent_high_lookback_trading_days`
  `price_state.min_trading_days_between_adds`

## State Boundary

Treat `SKILL.md` as strategy configuration only. Do not store live account state in this file.

- `SKILL.md` is the source of truth for strategy rules, thresholds, schedules, and default initialization values.
- SQLite is the source of truth for live account state and history.
- Real account fields such as `cash_pool`, `position_units`, `avg_cost_price`, `account_id`, and executed trades must live in the database, not in `SKILL.md`.
- `capital.initial_cash` is only the default starting amount used when initializing a new strategy account.
  It is not the current live cash balance after trading starts.
- After an account exists, update live state only through:
  `python {baseDir}/scripts/manage_strategy_account.py ...`
  `python {baseDir}/scripts/record_strategy_trade.py ...`
  `python {baseDir}/scripts/confirm_strategy_action.py ...`
- Do not edit `capital.initial_cash` in `SKILL.md` to reflect a new live balance.
  If the user adds cash or changes holdings, write that change to SQLite instead.

## Required Inputs

Do not invent missing inputs. If a required field is unavailable, return `skip_data_missing` and explain what is missing.

Required runtime inputs:

- `fund_code`
- `current_price`
- `cost_price`
- `cash_pool`
- `position_value`
- `recent_high`
- `today`
- `trade_time_local`
- `last_add_trade_date`
- `is_weekly_dca_day`
- `is_monthly_cash_inflow_day`

Derived values:

- `total_asset = cash_pool + position_value`
- `position_ratio = position_value / total_asset`
- `drawdown_pct = (recent_high - current_price) / recent_high * 100`
- `profit_pct = (current_price - cost_price) / cost_price * 100`
- `effective_fee_rate_pct = imported fund current_rate when available`

## Daily Workflow

1. Refresh or read fund data.
   For Eastmoney price data, run `python {baseDir}/scripts/import_eastmoney_pingzhongdata.py 011598` or replace `011598` with another fund code.
2. If today and the current local time match the configured `weekly_pretrade_reminder`, issue the weekly pretrade reminder.
3. If today and the current local time match the configured `weekly_trade_reminder`, issue the trading reminder and then evaluate the strategy.
4. If today and the current local time match the configured `monthly_cash_inflow_reminder`, remind the user to add the monthly cash inflow.
5. Record the monthly cash inflow only after it is actually added to `cash_pool`.
   Use `python {baseDir}/scripts/record_strategy_trade.py 011598 --trade-type cash_inflow --gross-amount 1000`.
6. Update `current_price`, `recent_high`, `total_asset`, and `position_ratio`.
7. Evaluate take-profit rules first when both buy and sell could trigger on the same day.
8. Evaluate dip-buy rules only if the add-spacing rule is satisfied and cash is available.
9. Evaluate weekly DCA only if no higher-priority trade was selected.
10. Re-check max and min position limits after sizing the candidate trade.
11. Execute at the configured cutoff rule.
   For backtests, prefer `next_trading_day` execution to avoid future leakage.

## Scheduling Rules

- `weekly_pretrade_reminder.weekday` and `weekly_pretrade_reminder.time_local` control the weekly pretrade reminder schedule.
- `weekly_trade_reminder.weekday` and `weekly_trade_reminder.time_local` control the weekly trade reminder schedule.
- `weekly_dca.weekday` controls which weekday counts as the DCA trading day.
- `monthly_cash_inflow.schedule_type` controls the monthly cash-inflow date used by the strategy state.
- `monthly_cash_inflow_reminder.schedule_type` and `monthly_cash_inflow_reminder.time_local` control the monthly reminder trigger.
- Supported monthly `schedule_type` values are:
  - `second_to_last_business_day`
  - `last_business_day`
  - `day_of_month`
- When `schedule_type = day_of_month`, fill `day_of_month` with an integer such as `15` or `28`.

## Decision Rules

### DCA

- Use `weekly_dca_amount` as the fixed recurring DCA amount.
- Size the actual DCA as `min(weekly_dca_amount, cash_pool)`.
- Skip DCA if there is already a higher-priority trade on the same day.

### Dip Buy

- Compute `drawdown_pct` from `recent_high`.
- Use only the deepest triggered threshold from `dip_thresholds_pct`.
- Map that threshold to the aligned base amount in `dip_base_buy_amounts`.
- Size the actual buy as the minimum of:
  - base buy amount
  - available `cash_pool`
  - remaining room under `max_position_ratio_pct`
- Reject the dip buy if the last add trade is within `min_trading_days_between_adds`.

### Take Profit

- Use only the highest triggered threshold from `profit_thresholds_pct`.
- Map that threshold to the aligned sell ratio in `profit_sell_ratios_pct`.
- Size the actual sell so the post-trade position ratio does not go below `min_position_ratio_pct`.
- Send sell proceeds back into `cash_pool`.

### Position And Cash Controls

- Keep all buys funded by `cash_pool`.
- Keep monthly inflows and sell proceeds inside `cash_pool`.
- Never exceed `max_position_ratio_pct`.
- Never reduce below `min_position_ratio_pct`.
- Include the imported fund `current_rate` in trade sizing when the user requires fees.

## Fund Detail Reporting

- Use `python {baseDir}/scripts/report_fund_details.py 011598 --refresh` to fetch and summarize a fund.
- Include the latest available fund identity, fee rate, minimum subscription, net worth, recent 20-trading-day high, drawdown, return metrics, stock-position estimate, manager information, asset allocation, holder structure, and top holdings.
- If local data is missing, allow the reporting script to refresh the SQLite database first.

## Drawdown Alerts

- Use `python {baseDir}/scripts/check_fund_alert.py 004475` to check drawdown alerts against the configured `dip_thresholds_pct` tiers in `SKILL.md`.
- To override the default tiers at runtime, repeat `--threshold-pct`, for example:
  `python {baseDir}/scripts/check_fund_alert.py 004475 --threshold-pct 5 --threshold-pct 10 --threshold-pct 15`
- This script only computes the alert state and returns structured output.
- Do not implement email or Feishu delivery inside this skill.
  If the user wants delivery, hand the alert result to the dedicated notification skill instead.

## Strategy Runtime Commands

Default SQLite location:

- `~/.fund_buying_decision/fund_buying_decision.db`
- Use `--db ~/.fund_buying_decision/<name>.db` when you want a separate database file for another account set or experiment.

- Initialize or overwrite the stored account state:
  `python {baseDir}/scripts/manage_strategy_account.py upsert 011598 --account-id main --cash-pool 1000 --position-units 0 --fund-type equity_fund`
- Record a real cash flow or manual trade:
  `python {baseDir}/scripts/record_strategy_trade.py 011598 --account-id main --trade-type cash_inflow --gross-amount 1000`
- Generate reminders and evaluate the strategy:
  `python {baseDir}/scripts/evaluate_strategy.py 011598 --account-id main --refresh`
- Confirm and execute the currently suggested strategy trade only after the user agrees:
  `python {baseDir}/scripts/confirm_strategy_action.py 011598 --account-id main --refresh --expected-action buy_dca`
- Check whether a drawdown alert is triggered:
  `python {baseDir}/scripts/check_fund_alert.py 004475`

## References To Load

- `references/strategy_parameters.md`
  Use when revising thresholds, clarifying formulas, or resolving ambiguous parameter choices.
- `references/data_inputs.md`
  Use when working with the SQLite importer, mapping database tables to strategy inputs, planning the next strategy-state tables, or assembling a fund detail report.
