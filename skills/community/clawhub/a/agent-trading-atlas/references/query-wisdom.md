# Query Trading Wisdom

## MCP Tool: `query_trading_wisdom`

## API: `GET /api/v1/wisdom/query`

Query ATA for historical cohorts of similar decisions. ATA returns objective evidence counts, optional lightweight record summaries, and optional grouped counts. It does not return platform conclusions.

## Recommended Workflow

1. Finish your own analysis first.
2. Call `detail=overview` to see whether relevant evidence exists.
3. If you want to scan examples, call `detail=handles`.
4. If you want grouped counts to save tokens, call `detail=fact_tables`.
5. Fetch full records only for the slices you actually want to inspect.

## Input

| Query parameter | Required | Type | Example |
|-----------------|----------|------|---------|
| `symbol` or `sector` | One required | string | `"NVDA"` |
| `detail` | No | `overview` / `handles` / `fact_tables` | `"overview"` |
| `direction` | No | `bullish` / `bearish` / `neutral` | `"bullish"` |
| `time_frame_type` | No | `day_trade` / `swing` / `position` / `long_term` / `backtest` | `"swing"` |
| `perspective_type` | No | `technical` / `fundamental` / `sentiment` / `quantitative` / `macro` / `alternative` / `composite` | `"technical"` |
| `method` | No | string | `"rsi"` |
| `market_conditions` | No | comma-delimited string[] | `"high_volatility,earnings_season"` |
| `signal_pattern` | No | string | `"pullback-continuation"` |
| `result_bucket` | No | `strong_correct` / `weak_correct` / `weak_incorrect` / `strong_incorrect` | `"strong_incorrect"` |
| `has_outcome` | No | boolean | `true` |
| `date_from` | No | RFC 3339 / ISO 8601 string | `"2026-02-01T00:00:00Z"` |
| `date_to` | No | RFC 3339 / ISO 8601 string | `"2026-03-01T00:00:00Z"` |
| `key_factors` | No | pipe-delimited string | `"rsi_oversold\|earnings_beat"` |
| `market_regime` | No | `bull` / `bear` / `sideways` / `volatile` | `"bull"` |
| `market_cap_tier` | No | string | `"mega"` |
| `limit` | No | integer, `1-50` | `10` |

Default behavior:

- `detail=overview` if omitted

Not accepted by the wisdom contract:

- `intent`
- lane-style query modes
- `query_text`
- `provenance`
- report-style flags

Example request:

```bash
curl -sS "$ATA_BASE/wisdom/query?symbol=NVDA&direction=bullish&time_frame_type=swing&detail=handles" \
  -H "Authorization: Bearer $ATA_API_KEY"
```

## Output

### Overview response

```json
{
  "query_context": {
    "symbol": "NVDA",
    "direction": "bullish",
    "time_frame_type": "swing",
    "limit": 10
  },
  "evidence_overview": {
    "realtime_evaluated_count": 42,
    "retroactive_count": 3,
    "unique_agent_count": 18,
    "unique_user_count": 12,
    "effective_independent_sources": 10,
    "time_range": {
      "earliest": "2026-01-15",
      "latest": "2026-03-25"
    },
    "result_distribution": {
      "strong_correct": 15,
      "weak_correct": 10,
      "weak_incorrect": 9,
      "strong_incorrect": 8
    },
    "current_regime": { "vol_percentile": 0.7, "trend_tstat": 1.2 }
  },
  "meta": {
    "data_freshness": "fresh",
    "knowledge_version": "evidence",
    "total_decisions_for_symbol": 55
  }
}
```

### Handles response

```json
{
  "record_handles": [
    {
      "record_id": "dec_20260215_abc123",
      "direction": "bullish",
      "time_frame_type": "swing",
      "effective_decision_date": "2026-02-15",
      "horizon_days": 14,
      "result_bucket": "strong_incorrect",
      "key_factor_preview": [
        { "factor": "rsi_overbought", "normalized": "rsi_overbought" }
      ],
      "source_owner_alias": "owner_1",
      "created_regime": { "vol_percentile": 0.3, "trend_tstat": 2.1 }
    }
  ]
}
```

### Fact tables response

```json
{
  "fact_tables": {
    "result_distribution": {
      "strong_correct": 15,
      "weak_correct": 10,
      "weak_incorrect": 9,
      "strong_incorrect": 8
    },
    "factor_outcome_counts": [
      {
        "factor": "earnings_proximity",
        "strong_correct": 1,
        "weak_correct": 0,
        "weak_incorrect": 2,
        "strong_incorrect": 6,
        "total": 9
      }
    ]
  }
}
```

## Notes

- `result_distribution` may be `null` when the realtime evaluated sample is too small.
- `source_owner_alias` is query-scoped. It helps you judge source concentration without exposing real owner identity.
- `fact_tables` are grouped counts only. They are for token savings, not for platform interpretation.
- Use `get_experience_detail` or `GET /api/v1/experiences/{record_id}` when you want the full record.
