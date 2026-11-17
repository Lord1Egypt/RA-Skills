## Description:

Provides real-time cryptocurrency market briefings with BTC/ETH/SOL prices, sentiment and cycle indicators, policy and blockchain news, and trending coin data from Desk3 APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desk3](https://clawhub.ai/user/desk3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch concise live cryptocurrency market briefings, including prices, sentiment, technical cycle indicators, news, exchange rates, market calendar items, and trending coins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Desk3 domains and depends on availability and accuracy of those external market-data APIs.

Mitigation: Run it only where outbound requests to Desk3 domains are approved, and verify important market values against trusted primary sources before acting on them.

Risk: Indicator text may sound like trading guidance, including buy, hold, or sell language.

Mitigation: Treat outputs as market information, not professional financial advice, and require human review before investment or trading decisions.

Risk: The skill defaults output formatting and content language to English.

Mitigation: Confirm that English output is acceptable for the target users or adapt invocation and review practices for other language needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/desk3/skills/cryptocurrency-market-live-briefing)
- [Desk3 website](https://www.desk3.io)
- [Desk3 market data API base](https://api1.desk3.io/v1/)
- [Desk3 MCP service API base](https://mcp.desk3.io/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with shell command examples and console text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; fetches public Desk3 API data with English language headers; no API key was detected.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
