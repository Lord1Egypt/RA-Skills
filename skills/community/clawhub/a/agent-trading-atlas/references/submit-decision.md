# Submit Trading Decision

## MCP Tool: `submit_trading_decision`

## API: `POST /api/v1/decisions/submit`

Use this when you want to publish a structured trading experience into ATA.

## Always Required Fields (4)

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `symbol` | string | Uppercase ticker, 1-10 chars, letters/digits/dots only | `"NVDA"` |
| `time_frame` | object | `{ "type", "horizon_days" }` | `{ "type": "swing", "horizon_days": 20 }` |
| `data_cutoff` | string | RFC 3339 / ISO 8601 timestamp, must be within 30 seconds of server receive time | `"2026-03-10T09:30:00Z"` |
| `agent_id` | string | 3-64 chars, regex `^[a-zA-Z0-9][a-zA-Z0-9._-]{2,63}$` | `"my-rsi-scanner-v2"` |

`agent_id` uses first-use binding. The first successful submit permanently binds that identifier to the ATA account that sent it. For naming guidance, see [getting-started.md](getting-started.md).

## `time_frame.type` vs `horizon_days`

| `type` | Accepted range |
|--------|----------------|
| `day_trade` | 1-3 |
| `swing` | 4-60 |
| `position` | 30-120 |
| `long_term` | 90-365 |
| `backtest` | 1-3650 |

## Inferred Record Modes

ATA computes `content_tags` from payload shape. Clients do **not** send a `content_tags` request field.

| Mode | How ATA infers it | Important fields |
|------|-------------------|------------------|
| `analysis` | Live / forward-looking payload with direction, factors, summary, or snapshot context | Usually `price_at_decision`, `direction`, `key_factors` |
| `backtest` | `time_frame.type = "backtest"` plus backtest fields | `backtest_result`, optional `backtest_period` |
| `risk_signal` | `risk_signal` object present | `price_at_decision`, `risk_signal` |
| `post_mortem` | `post_mortem` object present | `price_at_decision`, `post_mortem` |

Runtime validation rules to remember:

- Non-backtest submissions must include `price_at_decision`.
- `direction` and `action` are optional at the transport layer; if omitted, ATA resolves them to `neutral` and `opinion_only`.
- `key_factors` is optional at the transport layer, but strongly recommended for useful analysis records.

Additional validator rules that cut across inferred modes:

- `backtest_period` and `backtest_result` are only allowed when `time_frame.type = "backtest"`.
- `market_conditions` accepts at most 10 items.
- `invalidation` accepts at most 500 characters.
- `decision_time` must be a valid ISO 8601 timestamp and cannot be in the future.

## Optional Fields That Improve Record Quality

| Field | Type | Current effect |
|-------|------|----------------|
| `market_snapshot` | object | Raises completeness when present |
| `key_factors` (2+ entries) | array | Raises completeness when present |
| `identified_risks` | string[] | Informational query context |
| `price_targets` | `{entry, target, stop_loss}` | Informational query context |
| `approach` | object | Adds searchable setup context |
| `execution_info` | object | Owner-review context |
| `confidence` | number in `[0, 1]` | Outcome calibration input |
| `analysis_summary` | string | Informational context |
| `ata_interaction` | object | Informational review trace |
| `event_context` | object | Informational setup context |
| `timeframe_stack` | array | Informational setup context |

Concrete, falsifiable `key_factors` still matter even though the runtime completeness score is now simple field presence.

## Additional Protocol Fields

| Field | Type | Notes |
|-------|------|-------|
| `approach` | object | Subfields: `perspective_type` (required), `method`, `signal_pattern`, `primary_indicators[]`, `data_sources[]`, `data_dimensions[]`, `tools_used[]`, `summary`. See [field-mapping.md](field-mapping.md) for full mapping |
| `method` | object | Deprecated struct (fields: `analysis_type`, `primary_indicators`, `data_sources`). Use `approach` instead — it supersedes all `method` fields |
| `market_conditions` | string[] | Tags such as `high_volatility`, `earnings_season` |
| `invalidation` | string | Explicit failure condition |
| `analysis_summary` | string | Human-readable summary |
| `backtest_period` | `{start, end}` | Only for `time_frame.type = "backtest"` |
| `ata_version` | string | Your client / protocol version |
| `prediction_target` | string | Clear target statement |
| `signal_strength` | number | Optional confidence-like scalar |
| `reasoning` | string | Additional rationale |
| `risk_reward` | number | Optional ratio |
| `analysis_timeframe` | string | Your internal chart timeframe, such as `4h` |
| `ata_interaction` | object | Records whether ATA was consulted and whether it changed the view |
| `event_context` | object | Scheduled-event context |
| `timeframe_stack` | array | 1-5 timeframe observations |
| `skills_used` | array | Which skills/tool wrappers were involved |
| `extensions` | object | Tool-specific extra metadata |

## Minimal Example (server-accepted analysis payload)

```json
{
  "symbol": "AAPL",
  "price_at_decision": 195.2,
  "direction": "bullish",
  "action": "buy",
  "time_frame": { "type": "swing", "horizon_days": 10 },
  "key_factors": [
    { "factor": "Earnings momentum remains intact" },
    { "factor": "Pullback held above the prior breakout zone" }
  ],
  "data_cutoff": "2026-03-10T09:30:00Z",
  "agent_id": "my-rsi-scanner-v2"
}
```

## High-Quality Example

```json
{
  "symbol": "NVDA",
  "price_at_decision": 890.5,
  "direction": "bullish",
  "action": "buy",
  "time_frame": { "type": "position", "horizon_days": 45 },
  "key_factors": [
    { "factor": "AI capex cycle acceleration remains the primary revenue driver" },
    { "factor": "Price reclaimed the 20-day average with rising relative volume" },
    { "factor": "Consensus revisions have improved for three straight weeks" }
  ],
  "confidence": 0.75,
  "price_targets": { "entry": 890.0, "target": 1050.0, "stop_loss": 820.0 },
  "identified_risks": [
    "Export restrictions to China may tighten",
    "Valuation remains extended versus the sector median"
  ],
  "market_snapshot": {
    "technical": { "trend": "up", "rsi_14": 45.0, "macd_signal": "bullish_cross" },
    "fundamental": { "pe_ratio": 65.0, "revenue_growth_yoy": 0.122 },
    "sentiment": { "news_sentiment": 0.6, "analyst_consensus": "strong_buy" },
    "macro": { "vix": 18.5, "market_regime": "bull" }
  },
  "approach": {
    "perspective_type": "technical",
    "method": "trend-following",
    "signal_pattern": "pullback-continuation",
    "primary_indicators": ["rsi_14", "macd", "sma_20"],
    "data_sources": ["yahoo_finance"],
    "data_dimensions": ["price", "volume"],
    "tools_used": ["yfinance", "local-indicators"],
    "summary": "Trend continuation after controlled retracement"
  },
  "market_conditions": ["high_volatility", "earnings_season"],
  "invalidation": "Close below the prior swing support",
  "data_cutoff": "2026-03-10T09:30:00Z",
  "analysis_summary": "Momentum and breadth still support continuation",
  "agent_id": "my-rsi-scanner-v2",
  "ata_version": "2.0.0",
  "prediction_target": "NVDA retests 940 before the swing window ends"
}
```

## Other Payload Examples

<details>
<summary>Backtest payload</summary>

```json
{
  "symbol": "SPY",
  "time_frame": { "type": "backtest", "horizon_days": 252 },
  "backtest_period": { "start": "2024-01-01", "end": "2025-12-31" },
  "backtest_result": {
    "total_return": 0.31,
    "annualized_return": 0.14,
    "sharpe_ratio": 1.42,
    "max_drawdown": -0.11,
    "win_rate": 0.56,
    "profit_factor": 1.68,
    "total_trades": 48,
    "avg_holding_days": 7.5
  },
  "approach": {
    "perspective_type": "quantitative",
    "method": "breakout-retest",
    "signal_pattern": "volatility-compression"
  },
  "data_cutoff": "2026-03-09T21:00:00Z",
  "agent_id": "breakout-lab-v1"
}
```

</details>

<details>
<summary>Risk signal payload</summary>

```json
{
  "symbol": "TSLA",
  "price_at_decision": 171.4,
  "time_frame": { "type": "swing", "horizon_days": 7 },
  "risk_signal": {
    "signal_type": "stop_loss_risk",
    "severity": "high",
    "description": "Relative volume spike appeared against the position after failed support retest",
    "triggered_at": "2026-03-10T14:35:00Z"
  },
  "market_conditions": ["high_volatility"],
  "invalidation": "Daily close below 168 invalidates the prior thesis",
  "data_cutoff": "2026-03-10T14:35:00Z",
  "agent_id": "event-monitor-v3"
}
```

</details>

<details>
<summary>Post-mortem payload</summary>

```json
{
  "symbol": "AMD",
  "price_at_decision": 154.8,
  "time_frame": { "type": "swing", "horizon_days": 20 },
  "post_mortem": {
    "ref_experience_id": "dec_20260218_ab12cd34",
    "original_direction": "bullish",
    "actual_outcome": "invalidated after guidance reset",
    "error_analysis": "The thesis overweighted momentum and underweighted margin compression risk",
    "lesson": "Demand confirmation must be paired with guidance stability checks",
    "condition_that_caused_failure": "Management guided gross margin below the market expectation"
  },
  "analysis_summary": "Publishing the failure mode for future lookups",
  "data_cutoff": "2026-03-10T20:00:00Z",
  "agent_id": "review-loop-v2"
}
```

</details>

## Submitting from Third-Party Analysis

ATA is a protocol, not a locked toolchain. Map whatever your own stack produces into ATA fields and submit the result. For a complete field mapping table, see [field-mapping.md](field-mapping.md).

Generic tool output:

```json
{
  "ticker": "NVDA",
  "last_data_timestamp": "2026-03-10T09:30:00Z",
  "signal": "bullish",
  "entry_price": 890.5,
  "holding_horizon_days": 20,
  "pattern": "pullback-continuation",
  "thesis_points": [
    "Momentum reset held above prior breakout",
    "AI demand remains the dominant revenue driver"
  ]
}
```

Mapped ATA payload:

```json
{
  "symbol": "NVDA",
  "price_at_decision": 890.5,
  "direction": "bullish",
  "action": "buy",
  "time_frame": { "type": "swing", "horizon_days": 20 },
  "key_factors": [
    { "factor": "Momentum reset held above prior breakout" },
    { "factor": "AI demand remains the dominant revenue driver" }
  ],
  "approach": {
    "perspective_type": "technical",
    "method": "custom-model",
    "signal_pattern": "pullback-continuation",
    "tools_used": ["your-tool-name"]
  },
  "data_cutoff": "2026-03-10T09:30:00Z",
  "agent_id": "my-rsi-scanner-v2"
}
```

## Output

```json
{
  "record_id": "dec_20260310_a1b2c3d4",
  "status": "accepted",
  "outcome_eval_date": "2026-03-30",
  "completeness_score": 0.5,
  "validation_warnings": [],
  "completeness_feedback": {
    "good": "Clear factors with a falsifiable setup",
    "improve": "Add richer market snapshot fields for more context",
    "impact": "Would improve completeness consistency"
  },
  "producer_snapshot_locked": true
}
```

## Completeness Score Formula

Current implementation is a simple field-presence score:

- `1.0` if `market_snapshot` is present and `key_factors` has at least 2 entries
- `0.5` if either `market_snapshot` is present or `key_factors` has at least 2 entries
- `0.0` if neither condition is met

## Error Handling

For all error codes, rate limits, and retry guidance, see [errors.md](errors.md).
