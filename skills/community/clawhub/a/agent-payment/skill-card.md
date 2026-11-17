## Description:

Agent Payment helps autonomous agents create an EVM wallet, buy USDC-denominated AgentPMT credits through x402, sign authenticated requests, and check credit balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill to connect agents to AgentPMT wallet, credit-purchase, request-signing, tool-invocation, and balance-check workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to spend AgentPMT credits and sign wallet or payment messages.

Mitigation: Require explicit approval and a clear budget for every purchase, and use a fresh limited wallet.

Risk: Remote wallet generation and signing flows can expose private keys, mnemonics, session secrets, or unintended signatures if handled carelessly.

Mitigation: Store secrets only in a secret manager, avoid funding the generated wallet with unrelated assets, and sign only messages that exactly match local intent.

Risk: External endpoints, schemas, and dependencies may change over time.

Mitigation: Pin dependencies in an isolated environment and refresh the skill before relying on endpoints, schemas, setup steps, or examples.

## Reference(s):

- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api)
- [AgentPMT Marketplace](https://www.agentpmt.com)
- [Agent Payment ClawHub Listing](https://clawhub.ai/agentpmt/skills/agent-payment)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, shell, and signed-message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes HTTP request examples and EIP-191 signing templates for AgentPMT wallet, credit, session, tool invocation, and balance workflows.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
