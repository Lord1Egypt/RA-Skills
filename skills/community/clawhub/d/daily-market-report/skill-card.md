## Description: <br>
Generate daily US stock market analysis reports for user holdings, including portfolio P&L, 52-week range, analyst ratings, and actionable suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heiheiheibj](https://clawhub.ai/user/heiheiheibj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors or finance-focused agents use this skill to generate a daily text report for configured holdings and broad US market ETFs, including P&L, market metrics, analyst signals, and non-advisory suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports an undisclosed Finnhub script with a hardcoded credential. <br>
Mitigation: Review the packaged scripts before installation and prefer a release that removes embedded credentials and documents all outbound providers. <br>
Risk: Security evidence reports a runtime package installation fallback. <br>
Mitigation: Install dependencies explicitly in a controlled environment before running the report script. <br>
Risk: Finance tickers and holdings may be sent to third-party market data services. <br>
Mitigation: Use only holdings data that can be shared with the configured providers and confirm outbound network access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heiheiheibj/daily-market-report) <br>
- [Publisher profile](https://clawhub.ai/user/heiheiheibj) <br>
- [OpenClaw package requirement: yfinance](artifact/SKILL.md) <br>
- [ClawHub installation metadata](evidence.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text market report with setup and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured ticker holdings and prints portfolio metrics, market overview, analyst signals, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
