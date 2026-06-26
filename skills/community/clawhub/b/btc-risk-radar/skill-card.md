## Description: <br>
Professional BTC risk radar using public options, perp, and spot data. Use when the user wants a clear Bitcoin risk snapshot with volatility/skew context, panic or black-swan validation, timestamped evidence, confidence scoring, and explicit caveats for traders or advanced observers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, and advanced market observers use this skill to generate a timestamped Bitcoin risk-state snapshot from public options, perpetual, and spot-market data. It summarizes volatility, skew, funding, liquidity, confidence, caveats, and 72-hour validation triggers without placing trades or accessing private accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests to public crypto-market APIs may be blocked, intermittently unavailable, or inappropriate in restricted network environments. <br>
Mitigation: Run the skill only where public market API calls are allowed, and preserve the availability, data_gaps, degraded_mode, and confidence fields when explaining results. <br>
Risk: Heuristic risk labels and action triggers may be mistaken for deterministic predictions or financial advice. <br>
Mitigation: Present outputs as informational market-risk analysis, include explicit caveats and confidence, and do not use the skill to automatically trade or place orders. <br>
Risk: Providing exchange credentials, wallet access, cookies, or API keys would exceed the intended read-only public-data scope. <br>
Mitigation: Do not provide credentials or wallet access; use only the documented public data sources. <br>


## Reference(s): <br>
- [Metrics Reference](references/metrics.md) <br>
- [BTC Risk Radar ClawHub Page](https://clawhub.ai/spyfree/btc-risk-radar) <br>
- [Deribit Public API](https://www.deribit.com/api/v2/public) <br>
- [Coinbase BTC-USD Spot Public API](https://api.coinbase.com/v2/prices/BTC-USD/spot) <br>
- [Binance Public API](https://api.binance.com/api/v3) <br>
- [OKX Public API](https://www.okx.com/api/v5) <br>
- [Bybit Public API](https://api.bybit.com/v5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text narrative with optional JSON payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes as-of timestamp, source availability, data gaps, degraded-mode flag, confidence score, risk label, validation matrix, action triggers, and caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
