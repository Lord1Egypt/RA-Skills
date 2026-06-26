## Description: <br>
Comprehensive financial intelligence hub for SEC filings, crypto on-chain data, news sentiment, macro indicators, and global stock markets across the US, China, Hong Kong, Taiwan, Japan, and Korea. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuan622](https://clawhub.ai/user/xuan622) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve public financial data, SEC filings, crypto market signals, financial news sentiment, and macroeconomic indicators for research and analysis. It is informational only and does not execute trades or provide financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional API keys may be exposed through raw error output or shared logs. <br>
Mitigation: Use dedicated low-privilege API keys, avoid pasting logs or transcripts containing failed API calls, and rotate keys if exposure is suspected. <br>
Risk: Queries are sent to third-party financial data providers. <br>
Mitigation: Use the skill for public market research and avoid entering private portfolio details, proprietary trading strategies, or sensitive business information. <br>
Risk: Financial data from third-party APIs may be delayed, incomplete, or inaccurate. <br>
Mitigation: Verify critical facts with official sources before making financial, investment, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuan622/fin-intel-hub) <br>
- [README](README.md) <br>
- [Safety and Compliance Documentation](SAFETY.md) <br>
- [Security Status](SECURITY.md) <br>
- [Alpha Vantage API Key Documentation](https://www.alphavantage.co/support/#api-key) <br>
- [NewsAPI Registration](https://newsapi.org/register) <br>
- [FRED API Key Documentation](https://fred.stlouisfed.org/docs/api/api_key.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, configuration guidance, and structured data returned by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on public third-party financial APIs and optional user-provided API keys.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
