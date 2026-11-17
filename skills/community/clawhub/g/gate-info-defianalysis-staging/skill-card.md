## Description:

DeFi ecosystem analysis via Gate-Info MCP for TVL rankings, protocol metrics, yield/APY, stablecoins, bridges, exchange reserves, and liquidation heatmaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route DeFi market questions to read-only Gate Info MCP tools and produce neutral reports on protocol metrics, yields, stablecoins, bridges, exchange reserves, or liquidation data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat APY, reserve, liquidation, or protocol metrics as financial advice.

Mitigation: Keep outputs neutral and explicitly label results as informational, not investment advice.

Risk: Broad finance or yield prompts may be routed to this DeFi-specific skill when the user intent is unclear.

Mitigation: Ask whether the user means DeFi before using the skill for generic yield or finance questions.

Risk: Required Gate Info MCP tools may be unavailable or return partial data.

Mitigation: Degrade gracefully, label unavailable dimensions clearly, and avoid fabricating missing data.

## Reference(s):

- [Gate Info DeFi Analysis Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with tables, concise analysis, source labels, and informational disclaimers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate Info MCP tool results; outputs are informational and not financial advice.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
