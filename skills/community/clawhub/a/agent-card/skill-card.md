## Description:

Manage prepaid virtual Visa cards for AI agents with AgentCard, including card creation, balance checks, card credential access when requested, checkout support, card closure, and support workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipeabellos](https://clawhub.ai/user/pipeabellos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an AI agent to AgentCard tools for creating and managing prepaid virtual Visa cards, checking balances and transactions, filling checkout forms, and handling account setup or support tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create spend-capable virtual payment cards and interact with checkout flows.

Mitigation: Confirm intent and funding amounts before creating cards or payment-related actions, and keep the user responsible for final checkout submission.

Risk: The skill can access full payment card details when explicitly requested.

Mitigation: Reveal PAN or CVV only after an explicit user request and prefer balance or summary tools when full credentials are not needed.

Risk: The CLI install path is mutable and depends on external Node package resolution.

Mitigation: Use a trusted, pinned installation of the AgentCard CLI where possible, avoid sudo, and verify the publisher and MCP endpoint before use.

Risk: Financial metadata may be exposed through card lists, balances, and transaction history.

Mitigation: Ask for confirmation before listing cards, transactions, balances, or other payment-related account details in shared or sensitive sessions.

## Reference(s):

- [AgentCard](https://agentcard.sh)
- [AgentCard MCP Server](https://mcp.agentcard.sh/mcp)
- [AgentCard MCP Server Setup](references/setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment-card summaries, balances, transaction information, setup instructions, and user-confirmation prompts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
