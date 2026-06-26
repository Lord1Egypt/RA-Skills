# Snapshot Schema

## Purpose

Preserve the retained V2 snapshot schema as the analytical output shape and persisted daily artifact.

## Top-level keys

- `date`
- `generated_at`
- `fx_rates`
- `groups`
- `summary`

## Group keys

- `cost_basis`
- `positions`
- `fund`
- `cash`
- `positions_value`
- `total_value`
- `profit`
- `return_pct`

## Position keys

- `name`
- `ticker`
- `quantity`
- `cost_price`
- `current_price`
- `currency`
- `fx_rate`
- `market_value_cny`
- `cost_value_cny`
- `profit_cny`
- `profit_pct`
- `weight_in_group` (deferred in phase 1)

## Summary keys

- `total_value`
- `total_cost`
- `total_profit`
- `total_return_pct`
- `daily_change`
- `daily_change_pct`
- `capital_change`
- `market_daily_change`
- `market_daily_change_pct`
- `max_drawdown_pct`
- `month_return_pct`
- `sharpe_ratio`
- `volatility_annual`
- `win_rate`
- `profit_loss_ratio`

Deferred in phase 1:
- `prev_date`
- `prev_total_value`
- `month_start_value`
- `month_change`
- `month_market_change`
- `avg_win_pct`
- `avg_loss_pct`
- `trading_days`
- `weight_in_group`

## Artifact rule

Snapshot is derived from holdings-based analysis. It is useful for cache, history, and quick reads, but it is not the authority.
