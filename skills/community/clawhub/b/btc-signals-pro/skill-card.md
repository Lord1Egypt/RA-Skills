## Description: <br>
Real-time Bitcoin trading intelligence API providing market data, AI trade signals, derivatives flow, liquidation heatmaps, live crypto news, economic calendar, historical OHLCV, and 50+ data sources for AI-driven trade decisions and automated trading bots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricklaughhunn](https://clawhub.ai/user/ricklaughhunn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to BTC Signals Pro for Bitcoin market snapshots, trade-signal summaries, derivatives and liquidity context, crypto news, macro calendar checks, and historical market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides trading outputs that may be incorrect, stale, or financially risky. <br>
Mitigation: Treat outputs as informational and manually review buy/sell levels, stop losses, and bot-pattern guidance before risking funds. <br>
Risk: The skill makes authenticated requests to BTC Signals Pro using BTC_SIGNALS_API_KEY. <br>
Mitigation: Keep the API key private, avoid printing it in chat, and monitor API usage. <br>
Risk: The skill depends on an external paid API and network availability. <br>
Mitigation: Confirm the subscription and key status before relying on responses, and handle failed or rate-limited API calls conservatively. <br>


## Reference(s): <br>
- [BTC Signals Pro API Reference](artifact/references/api-reference.md) <br>
- [BTC Signals Pro API](https://api.btcsignals.pro/v1) <br>
- [BTC Signals Pro pricing](https://btcsignals.pro/pricing) <br>
- [ClawHub release page](https://clawhub.ai/ricklaughhunn/btc-signals-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with API request examples, market-analysis narrative, and trading levels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BTC_SIGNALS_API_KEY for authenticated requests and should not print the full key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
