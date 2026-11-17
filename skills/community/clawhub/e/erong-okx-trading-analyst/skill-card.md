## Description:

OKX cryptocurrency technical analysis tool that retrieves market data, calculates indicators including moving averages, MACD, RSI, Bollinger Bands, and ATR, and generates trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze cryptocurrency pairs through OKX market data, technical indicators, and generated buy, sell, or hold-style signals. Its output is for market analysis and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary classifies the skill as suspicious because of under-disclosed command execution paths and exchange secret handling.

Mitigation: Review or fix the command-execution path before installation and run only vetted local scripts.

Risk: The skill handles OKX API credentials even though market-data analysis should only need read access.

Mitigation: Use read-only OKX credentials, avoid broad exchange permissions, and rotate credentials if they may have been exposed.

Risk: Untrusted symbols or timeframes can increase command-execution risk through wrapper behavior.

Mitigation: Pass only trusted symbols and timeframes, and validate inputs before invoking wrapper scripts.

Risk: Trading signals and technical analysis can be wrong or misleading in volatile cryptocurrency markets.

Mitigation: Treat outputs as informational analysis only and require human review before any trading decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erongcao/skills/erong-okx-trading-analyst)
- [Publisher profile](https://clawhub.ai/user/erongcao)
- [OKX API base URL](https://www.okx.com)
- [NS3 feed API](https://api.ns3.ai/feed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style console reports with trading signal summaries, indicator details, and optional notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require OKX credentials and network access to OKX and news APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
