## Description:

DeFi ecosystem analysis via Gate-Info MCP for TVL rankings, protocol metrics, yield/APY, stablecoins, bridges, exchange reserves, and liquidation heatmaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route DeFi market questions to read-only Gate-Info MCP tools and receive neutral markdown analysis of protocol, yield, bridge, reserve, stablecoin, and liquidation data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield, APY, liquidation, reserve, and protocol metrics can change quickly and may be misread as financial advice.

Mitigation: Label outputs as informational market data, include source and generated-time context where available, and avoid buy/sell or guaranteed-yield language.

Risk: The required Gate-Info MCP server or individual tools may be unavailable or return incomplete data.

Mitigation: Confirm the Gate-Info MCP server is configured before use; if a tool fails, label that section as unavailable and continue only with available documented data.

Risk: Calling tools outside the documented scenario can broaden data exposure or produce unsupported analysis.

Mitigation: Use only the Gate-Info MCP tools listed in the skill and route unrelated coin, technical, news, macro, or risk requests to the matching dedicated skill.

Risk: Users may over-rely on exchange reserve or liquidation heatmap outputs.

Mitigation: State that reserve data may not reflect total assets and that liquidation heatmaps are estimates, not guaranteed triggers.

## Reference(s):

- [Gate Info DeFi Analysis Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-info-defianalysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with tables, concise analysis, source notes, and risk disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gate-Info MCP data is summarized in the user's language; unsupported or failed data dimensions are labeled rather than fabricated.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
