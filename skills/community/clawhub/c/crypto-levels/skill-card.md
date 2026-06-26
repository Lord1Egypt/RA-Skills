## Description: <br>
Analyze cryptocurrency support and resistance levels, current prices, technical indicators, and trading insights for pairs such as BTC-USDT and ETH-USDT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[362224222](https://clawhub.ai/user/362224222) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and traders use this skill to generate cryptocurrency support and resistance analysis, technical indicators, and concise trading-oriented summaries. Developers can also run the included Python scripts for quick, manual, mock, or configured analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto analysis can be mistaken for financial advice or used with stale, mock, or default market data. <br>
Mitigation: Treat outputs as educational technical analysis only, verify prices independently, and do not rely on the skill as financial advice. <br>
Risk: Local Python scripts call public crypto market-data APIs and may require user-provided inputs or optional API configuration. <br>
Mitigation: Review scripts before execution, avoid trading-enabled exchange keys, and use only read-only or public market-data credentials when configuring data sources. <br>
Risk: Network availability, API rate limits, and data-source differences can affect price and level accuracy. <br>
Mitigation: Check timestamps and data-source status, compare multiple market sources for important decisions, and fall back to fresh manually supplied prices when API data is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/362224222/crypto-levels) <br>
- [Configuration Guide](references/CONFIGURATION.md) <br>
- [Supported Cryptocurrency Pairs](references/SUPPORTED_PAIRS.md) <br>
- [Technical Analysis Guide](references/TECHNICAL_GUIDE.md) <br>
- [CoinGecko](https://www.coingecko.com/) <br>
- [TradingView](https://www.tradingview.com/) <br>
- [Investopedia Support and Resistance](https://www.investopedia.com/terms/s/support.asp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style technical analysis with price levels, indicators, warnings, and optional inline shell commands or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use live public market-data APIs, manually supplied prices, or mock/offline demonstration data depending on the script and configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
