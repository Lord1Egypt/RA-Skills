## Description: <br>
Builds a Freqtrade 4h Bollinger-band mean-reversion strategy that trades long and short on 2-sigma band touches with RSI confirmation and an ADX < 25 range-regime gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to draft and configure a Freqtrade futures strategy for range-bound crypto markets. It provides strategy code, reference configuration, tunable parameters, backtest context, and deployment cautions for major pairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live financial automation can lose funds if exchange fees, slippage, liquidation behavior, or order execution differ from the backtest assumptions. <br>
Mitigation: Paper trade first and confirm exchange-specific fees, slippage, liquidation behavior, and order execution before any live deployment. <br>
Risk: The ROI ladder is central to the strategy, and ambiguity between strategy-level and config-level ROI settings can change live behavior. <br>
Mitigation: Resolve the ROI setting ambiguity before deployment so the live configuration matches the intended ladder. <br>
Risk: The strategy can fail during trend transitions, news spikes, and meme or low-cap pair volatility. <br>
Mitigation: Restrict deployment to validated major pairs, size positions conservatively, and consider pausing during scheduled macro events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/bollinger-reverter-4h) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown containing Python strategy code, JSON configuration, tables, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backtest results and trading-risk guidance; no API keys, credentials, MCP tools, or API calls were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
