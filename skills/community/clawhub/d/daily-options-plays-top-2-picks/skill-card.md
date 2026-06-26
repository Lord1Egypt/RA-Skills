## Description: <br>
Build a simple stock-options watchlist and paper-trade plan after the first 15 minutes of the market session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrmerced1292-commits](https://clawhub.ai/user/jrmerced1292-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create a concise, beginner-friendly U.S. stock-options paper-trade watchlist after the first 15 minutes of the trading session. It helps rank up to two setups with entry, stop, target, contract guidance, confidence, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Options-watchlist output may be mistaken for trade instructions or guaranteed financial advice. <br>
Mitigation: Use the output only for educational planning, keep paper-trade-first framing, and do not place trades solely from this skill's output. <br>
Risk: Market data, news, liquidity, implied volatility, and option-chain details may be stale, missing, or unavailable to the agent. <br>
Mitigation: Independently verify live prices, catalysts, liquidity, implied volatility, and option-chain data before relying on any setup. <br>


## Reference(s): <br>
- [Beginner Options Watchlist Framework](references/watchlist-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown watchlist with concise bullets and structured play notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits final trade ideas to the top two setups and defaults to paper-trade-first educational framing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
