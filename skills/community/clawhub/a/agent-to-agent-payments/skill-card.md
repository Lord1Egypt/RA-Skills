## Description:

Helps agents monetize services, create payment requests, and add autonomous payment flows using PayRam MCP across supported crypto networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to connect PayRam MCP, generate payment integration snippets, and design agent-to-agent billing, storefront, marketplace, and treasury workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous payment, signing, transfer, treasury, or other irreversible crypto actions may move funds without adequate review.

Mitigation: Require explicit human confirmation before creating, signing, transferring, or managing payments, and use least-privilege credentials or wallets.

Risk: The skill connects agents to a mutable remote MCP service whose available tools can change over time.

Mitigation: Review the remote MCP tools before enabling the skill and periodically re-check tool behavior after updates.

Risk: Generated SDK snippets may introduce unsafe or incorrect payment handling if executed without inspection.

Mitigation: Review generated code before use and test payment flows with low-value or sandbox-like setups before handling real funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/buddhasource/skills/agent-to-agent-payments)
- [PayRam Homepage](https://payram.com)
- [PayRam Documentation](https://docs.payram.com)
- [PayRam MCP Server](https://mcp.payram.com)
- [PayRam Helper MCP Server Repository](https://github.com/PayRam/payram-helper-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, MCP tool calls, and payment workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate SDK snippets and payment workflow recommendations; review before executing payment-related actions.]

## Skill Version(s):

1.1.3 (source: evidence release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
