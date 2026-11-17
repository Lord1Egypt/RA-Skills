## Description:

Crypto Market Analysis retrieves public Binance market data, calculates technical indicators such as MACD, KDJ, RSI, CCI, BOLL, WR, PSY, BRAR, and DMI, and prepares structured cryptocurrency market analysis prompts and reports for a user-connected LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunawolves07](https://clawhub.ai/user/lunawolves07)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts can use this skill to gather Binance public market data, calculate common technical indicators, and generate structured cryptocurrency analysis for selected symbols and time intervals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation of an unpinned Python package can change the runtime environment or pull unexpected dependency versions.

Mitigation: Use the skill only in an isolated Python environment where package installation is acceptable, or preinstall and pin TA-Lib through a controlled setup process.

Risk: Generated market analysis may be incomplete, inaccurate, or mistaken for financial advice.

Mitigation: Treat outputs as informational technical analysis, review conclusions before acting, and do not rely on the generated report as financial advice.

Risk: Requested symbols and intervals are sent to Binance public APIs.

Mitigation: Avoid using symbols or analysis patterns that should remain private, and account for Binance availability and rate limits.

## Reference(s):

- [Binance API Notes](references/binance_api_notes.md)
- [Technical Indicators](references/technical_indicators.md)
- [Binance Klines API](https://api.binance.com/api/v3/klines)
- [Binance 24hr Ticker API](https://api.binance.com/api/v3/ticker/24hr)
- [ClawHub Skill Page](https://clawhub.ai/lunawolves07/skills/crypto-market-analysis)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lunawolves07)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis report with JSON intermediate data and LLM prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Binance public API availability, selected trading symbol and intervals, TA-Lib availability, and the user's connected LLM.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
