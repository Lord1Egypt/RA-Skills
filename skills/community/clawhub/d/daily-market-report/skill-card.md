## Description:

Generate daily US stock market analysis reports for user holdings, including portfolio P&L, 52-week range, analyst ratings, and actionable suggestions. Data sourced from Yahoo Finance (yfinance, no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[heiheiheibj](https://clawhub.ai/user/heiheiheibj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily US market report for configured holdings and tracked market indices, including portfolio P&L, valuation metrics, analyst ratings, and action-oriented watch notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags unsafe remote shell and PowerShell installation commands.

Mitigation: Review installation steps before use and prefer a pinned, trusted installation method in an isolated environment.

Risk: The server security summary flags automatic package installation behavior.

Mitigation: Install reviewed dependencies explicitly before running the report script.

Risk: The server security summary flags an exposed undocumented API key in a bundled Finnhub script.

Mitigation: Do not run the bundled Finnhub script with the exposed key; use the documented yfinance-based report path instead.

## Reference(s):

- [Daily Market Report on ClawHub](https://clawhub.ai/heiheiheibj/skills/daily-market-report)
- [uv installer for macOS and Linux](https://astral.sh/uv/install.sh)
- [uv installer for Windows](https://astral.sh/uv/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text report with setup instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content depends on configured holdings, tracked indices, and live or recent Yahoo Finance market data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
