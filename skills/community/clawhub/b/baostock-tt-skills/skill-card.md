## Description:

Provides agent guidance and helper scripts for querying BaoStock A-share historical prices, financial data, macroeconomic data, sector constituents, and MyTT technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonpro22](https://clawhub.ai/user/jasonpro22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to have an agent retrieve China A-share market data through BaoStock and produce technical-analysis reports with MyTT indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data and technical-analysis output may be incomplete, stale, or mistaken for investment advice.

Mitigation: Treat outputs as informational, verify data independently, and avoid relying on generated buy/sell-style guidance as financial advice.

Risk: The skill installs and uses external Python packages and queries BaoStock, so behavior can depend on package versions and network/service availability.

Mitigation: Pin dependencies where possible, review package sources before installation, and confirm network access to BaoStock before operational use.

Risk: Full-market A-share scans can be long-running and may trigger rate limits or consume significant execution time.

Mitigation: Require explicit user confirmation, batch requests, show progress, and add delays for broad scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonpro22/skills/baostock-tt-skills)
- [BaoStock API reference included with artifact](artifact/docs/python_api_full.txt)
- [Artifact README](artifact/README.md)
- [MyTT project](https://github.com/mpquant/MyTT)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tabular market data summaries and technical-analysis signals.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
