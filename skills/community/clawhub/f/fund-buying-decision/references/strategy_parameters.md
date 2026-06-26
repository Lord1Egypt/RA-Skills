# Strategy Parameters

Use this file when the numeric block in `SKILL.md` needs clarification or refinement.

The YAML in `SKILL.md` is intentionally split into two top-level blocks:

- `editable`
  The user-facing values most likely to change.
- `fixed`
  Values that usually stay stable unless the strategy design changes.

At runtime, the loader merges `fixed` and `editable` back into one flat parameter map. The strategy code still reads `capital.*`, `scheduling.*`, `price_state.*`, `take_profit.*`, and `risk.*`.

## Frequently Adjusted By The User

- `capital.initial_cash`
  Starting cash pool used when a strategy account is initialized.
- `capital.weekly_dca_amount`
  Fixed weekly recurring buy size.
- `capital.monthly_cash_pool_inflow`
  Monthly cash amount the reminder asks the user to add.
- `scheduling.weekly_pretrade_reminder.*`
  Which weekday and time to issue the pretrade reminder.
- `scheduling.weekly_dca.weekday`
  Which weekday counts as the DCA day.
- `scheduling.weekly_trade_reminder.*`
  Which weekday and time to issue the trading reminder.
- `scheduling.monthly_cash_inflow.*`
  Which calendar rule marks the monthly cash-inflow date.
- `scheduling.monthly_cash_inflow_reminder.*`
  Which calendar rule and time mark the monthly reminder.
- `price_state.dip_thresholds_pct`
  Drawdown tiers that trigger dip buys.
- `price_state.dip_base_buy_amounts`
  Buy amounts aligned to each drawdown tier.
- `take_profit.profit_thresholds_pct`
  Profit tiers that trigger partial sells.
- `take_profit.profit_sell_ratios_pct`
  Sell ratios aligned to each profit tier.
- `risk.max_position_ratio_pct`
  Position cap after a buy.
- `risk.min_position_ratio_pct`
  Position floor after a sell.

## Usually Fixed Unless The Strategy Shape Changes

- `universe.allowed_fund_types`
- `universe.disallowed_fund_types`
- `capital.fee_rate_source`
- `scheduling.trade_cutoff_local_time`
- `scheduling.backtest_execution_mode`
- `scheduling.max_trades_per_day`
- `price_state.recent_high_lookback_trading_days`
- `price_state.min_trading_days_between_adds`

## Formula Notes

- `total_asset = cash_pool + position_value`
- `position_ratio = position_value / total_asset`
- `drawdown_pct = (recent_high - current_price) / recent_high * 100`
- `profit_pct = (current_price - cost_price) / cost_price * 100`

## Fixed Values Already Chosen

- `capital.initial_cash = 1000`
- `capital.weekly_dca_amount = 100`
- `capital.monthly_cash_pool_inflow = 1000`
- `capital.fee_rate_source = fund_current_rate`
- `scheduling.weekly_pretrade_reminder.weekday = monday`
- `scheduling.weekly_pretrade_reminder.time_local = 09:00`
- `scheduling.weekly_dca.weekday = tuesday`
- `scheduling.weekly_trade_reminder.weekday = tuesday`
- `scheduling.weekly_trade_reminder.time_local = 09:30`
- `scheduling.monthly_cash_inflow.schedule_type = second_to_last_business_day`
- `scheduling.monthly_cash_inflow.day_of_month = null`
- `scheduling.monthly_cash_inflow_reminder.schedule_type = second_to_last_business_day`
- `scheduling.monthly_cash_inflow_reminder.day_of_month = null`
- `scheduling.monthly_cash_inflow_reminder.time_local = 10:00`
- `price_state.recent_high_lookback_trading_days = 20`

## Default Database Location

- Default runtime database: `~/.fund_buying_decision/fund_buying_decision.db`
- Recommended override pattern when you want separate datasets: `--db ~/.fund_buying_decision/<name>.db`

## Interpretation Rules

- Treat `dip_thresholds_pct` and `dip_base_buy_amounts` as aligned arrays.
  Example: threshold `10` maps to base amount `150`.
- Treat `profit_thresholds_pct` and `profit_sell_ratios_pct` as aligned arrays.
  Example: profit `20` maps to sell ratio `20`.
- When multiple buy thresholds trigger on the same day, use only the deepest drawdown tier.
- When multiple sell thresholds trigger on the same day, use only the highest profit tier.
- When both a buy and a sell could trigger, prefer the sell because it reduces risk and preserves the one-trade-per-day rule.
- Reminder generation is schedule-driven.
  Weekly reminder weekday and time, plus the monthly reminder date rule and time, are configured in `SKILL.md`.
- Supported monthly reminder date rules are `second_to_last_business_day`, `last_business_day`, and `day_of_month`.
- If `day_of_month` is used, set the matching `day_of_month` integer in `SKILL.md`.

## Practical Defaults Already Set

- Initial cash: `1000`
- Weekly baseline DCA: `100`
- Monthly new cash to pool: `1000`
- Dip thresholds: `5 / 10 / 15`
- Dip base buy amounts: `100 / 150 / 200`
- Profit thresholds: `10 / 20`
- Profit sell ratios: `10 / 20`
- Position floor / cap: `20 / 80`

## Ambiguities Left Explicit On Purpose

- `weekly_dca_amount` and `monthly_cash_pool_inflow` can stay asymmetric.
  That is valid if the user wants new money to accumulate before dip-buy opportunities appear.
- `fee_rate_source = fund_current_rate` means the strategy should read the fund's imported current subscription rate from the Eastmoney payload instead of a single global hard-coded fee.
- `second_to_last_business_day` is currently approximated with Monday-Friday weekdays only.
