## Description: <br>
基于缠中说禅理论，分析走势中枢、笔分段、背驰判断和买卖点，并支持A股、港股、美股和加密货币。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanduan003](https://clawhub.ai/user/sanduan003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Traders, analysts, and developers use this skill to run Chan-theory technical analysis on public market symbols and review printed indicators for structure, divergence, and key price zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market analysis output can be incomplete, delayed, or misleading if public market data is unavailable or the indicator interpretation is used as financial advice. <br>
Mitigation: Treat the output as analysis support only, verify data and conclusions independently, and do not rely on it for automated trading decisions. <br>
Risk: The script installs and imports Python packages and contacts yfinance/Yahoo Finance for public market data. <br>
Mitigation: Install it in a Python virtual environment when possible, review the dependency command before running it, and run it only in environments where outbound public market-data requests are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanduan003/chan-theory-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/sanduan003) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with technical-analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data for supplied symbols and prints Chan-theory indicators, MACD values, and key price zones.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
