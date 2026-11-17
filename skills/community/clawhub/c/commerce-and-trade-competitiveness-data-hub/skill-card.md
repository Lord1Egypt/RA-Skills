## Description:

Commerce and Trade Competitiveness Data Hub lets an agent query World Bank TCdata360 trade and competitiveness data by country or region through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query trade data, benchmark country competitiveness, analyze export and import trends, compare regions, and review tariff, logistics, and trade-cost indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls go to AgentPMT's hosted service and may cost credits.

Mitigation: Confirm that AgentPMT is trusted and that the enabled Agent Group and credit usage are appropriate before use.

Risk: Prompts or logs could expose secrets or payment credentials.

Mitigation: Do not include account secrets, wallet private keys, signatures, payment headers, or credentials in prompts or logs.

Risk: Optional unpinned setup commands can change over time.

Mitigation: Prefer OpenClaw or pinned, reviewed setup commands before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/commerce-and-trade-competitiveness-data-hub)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/trade-competitiveness-data)
- [Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls to a hosted AgentPMT action that returns JSON trade and competitiveness data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
