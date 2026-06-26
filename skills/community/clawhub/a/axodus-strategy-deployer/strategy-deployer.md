# SKILL: strategy-deployer

## Purpose
Deploy trading strategies safely using an explicit lifecycle: validate → risk-check → paper deploy → monitor → (guarded) live promote → scale/stop.

## When to Use
- A strategy is ready after backtesting.
- Moving from research to paper trading.
- Promoting a paper-tested strategy to live trading (guarded).

## Inputs
- `strategy_spec` (required, object|string): rules, signals, markets, timeframes.
- `mode` (optional, enum: `paper|live`, default: `paper`)
- `risk_limits` (required, object): max risk per trade, max drawdown, exposure caps.
- `validation_artifacts` (optional, object): backtest report, paper performance stats.
- `approval` (optional, string): explicit user/Morpheus approval reference for `live`.

## Steps
1. Verify prerequisites:
   - strategy has a written hypothesis and defined invalidation conditions
   - backtest/paper artifacts exist (as applicable)
2. Run risk checks:
   - enforce risk per trade
   - enforce exposure caps
   - enforce max drawdown thresholds
   - ensure kill-switch is configured
3. Deploy to paper (default):
   - start with small allocation
   - emit logs for every signal and order
4. Monitor and record:
   - trades
   - slippage
   - drawdown
   - regime notes
5. Promote to live only if:
   - explicit `mode=live`
   - explicit approval is present
   - preflight checks pass
6. Define rollback/stop rules and execute them on trigger.

## Validation
- Paper mode produces complete logs and trade history entries.
- Live mode is blocked unless approval + flags are present.
- Risk constraints are enforced before every order.
- Stop conditions are tested (kill-switch works).

## Output
```yaml
deployment: "paper|live"
strategy: "<name/id>"
markets: ["..."]
risk_limits: { "...": "..." }
status: "deployed|blocked|stopped"
audit_events: ["signal_detected", "risk_check_passed", "order_submitted", "order_filled", "trade_recorded"]
```

## Safety Rules
- Never bypass risk checks to “capture opportunity”.
- Never deploy live without explicit approval and a paper validation phase.
- Never imply profit certainty; report performance as historical/conditional.

## Example
Paper deploy:
- `strategy_spec`: “Mean reversion in range regime, 5m timeframe.”
- `mode`: `paper`
- Output: deployment report + monitoring checklist + stop triggers.

