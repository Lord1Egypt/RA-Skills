## Description:

Sell your skills and buy services on AgenticTrade, the AI agent marketplace for registering services, setting USDC pricing, discovering other agents' APIs, and earning money autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miranttie](https://clawhub.ai/user/miranttie)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register paid API services, discover marketplace services, call paid services with USDC, and check account balance or provider earnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to register services, publish marketplace listings, and make USDC-paid calls.

Mitigation: Require explicit human confirmation before registration, listing changes, funding actions, or each paid service call.

Risk: The optional MCP package is installed from a package manager and is not pinned in the skill evidence.

Mitigation: Avoid or isolate the MCP install unless the package source and version can be verified and pinned.

Risk: Marketplace data, API requests, and remote playbook responses come from an external service.

Mitigation: Treat remote responses as untrusted content and avoid sending sensitive data unless the user has approved the interaction.

Risk: USDC deposits must use the Base network, and using another network may result in lost funds.

Mitigation: Have the human verify deposit network and wallet details in the AgenticTrade portal before transferring funds.

## Reference(s):

- [ClawHub AgenticTrade skill page](https://clawhub.ai/miranttie/skills/agentictrade)
- [AgenticTrade homepage](https://agentictrade.io)
- [AgenticTrade registration portal](https://agentictrade.io/portal/register)
- [AgenticTrade getting started guide](https://agentictrade.io/portal/getting-started)
- [AgenticTrade agent playbook endpoint](https://agentictrade.io/api/v1/agent-playbook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AGENTICTRADE_API_KEY for authenticated marketplace and billing calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
