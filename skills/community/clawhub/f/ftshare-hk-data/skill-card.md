## Description:

Fetches Hong Kong stock company profiles, valuation metrics, basic stock views, and daily, monthly, quarterly, or yearly candlestick history from market.ft.tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong stock-data questions about company introductions, valuation ratios, market capitalization, share counts, listing status, and historical OHLCV candles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python handlers and makes unauthenticated HTTPS requests to market.ft.tech.

Mitigation: Install only when that network behavior is acceptable, run with appropriate network controls, and review the included scripts before deployment.

Risk: The security guidance notes missing explicit permission metadata, request timeouts, response-size limits, and stricter redirect handling.

Mitigation: Add or enforce permission metadata, request timeouts, response-size limits, and strict redirect handling before broad deployment.

Risk: Market data freshness and availability depend on the external service and the Hong Kong exchange calendar; the artifact notes current-day candlestick updates after 18:00 UTC+8.

Mitigation: Have the agent state the source and effective date for returned data, handle API errors explicitly, and avoid presenting the output as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-hk-data)
- [market.ft.tech API host](https://market.ft.tech)
- [Company profile endpoint example](https://market.ft.tech/data/api/v1/market/data/hk/company-hk?trade_code=00700.HK)
- [Candlestick endpoint example](https://market.ft.tech/data/api/v1/market/data/hk/hk-candlesticks?trade_code=00700.HK&interval_unit=day&since_date=2026-03-01&until_date=2026-03-24&limit=20)
- [Valuation endpoint example](https://market.ft.tech/data/api/v1/market/data/hk/hk-valuatnanalyd?trade_code=00700.HK&page=1&page_size=20)
- [Basic stock view endpoint example](https://market.ft.tech/data/api/v1/market/data/hk/hk-view?hk_code=00700.HK)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses printed to stdout, with agent-facing text or Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on unauthenticated HTTPS responses from market.ft.tech; date fields are interpreted against the Hong Kong exchange calendar in UTC+8.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
