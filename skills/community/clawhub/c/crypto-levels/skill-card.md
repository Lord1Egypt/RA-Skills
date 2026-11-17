## Description:

Analyzes cryptocurrency price data to produce current price context, support and resistance levels, and technical-analysis insights for pairs such as BTC-USDT and ETH-USDT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[362224222](https://clawhub.ai/user/362224222)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to request cryptocurrency support and resistance levels, technical indicators, and brief trading context. The output is informational and educational, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading output may be mistaken for financial advice.

Mitigation: Treat the analysis as educational market context only and review decisions with qualified financial guidance before trading.

Risk: Predictable files in /tmp may matter on shared systems.

Mitigation: Run the skill as a normal, unprivileged user and avoid shared systems when temporary-file contents matter.

Risk: The packaging script can archive files outside the skill tree through symlinks.

Mitigation: Do not run package_skill.py on untrusted or modified skill directories; inspect symlinks before packaging.

Risk: External market-data APIs can be delayed, unavailable, rate-limited, or configured with sensitive keys.

Mitigation: Use documented data-source settings, keep API keys out of prompts and source files, and compare critical market data against independent sources.

## Reference(s):

- [Technical Analysis Guide](references/TECHNICAL_GUIDE.md)
- [Crypto Levels Configuration Guide](references/CONFIGURATION.md)
- [Supported Cryptocurrency Pairs](references/SUPPORTED_PAIRS.md)
- [Investopedia - Support and Resistance](https://www.investopedia.com/terms/s/support.asp)
- [Investopedia - Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)
- [Investopedia - Moving Average](https://www.investopedia.com/terms/m/movingaverage.asp)
- [TradingView - Chart Patterns](https://www.tradingview.com/chart-patterns/)
- [CoinGecko](https://www.coingecko.com/)
- [ClawHub Skill Page](https://clawhub.ai/362224222/skills/crypto-levels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style analysis with price levels, indicators, and inline shell commands for script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live API-derived market data or manual/offline analysis depending on configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
