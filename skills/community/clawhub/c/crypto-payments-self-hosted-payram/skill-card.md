## Description:

Helps agents and developers integrate PayRam as a self-hosted crypto and stablecoin payment gateway for USDT, USDC, Bitcoin, and ETH payments across supported networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:


## Use Case:

External developers and engineering teams use this skill to evaluate PayRam, run its MCP helper server, generate payment and webhook integration code, and scaffold payment-enabled starter applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run an external MCP server from an unpinned repository.

Mitigation: Pin the referenced repository to a reviewed commit and run the MCP server only in a sandbox or disposable development environment.

Risk: Codebase assessment and scaffolding tools may touch sensitive payment flows or project files.

Mitigation: Use a clean branch, review generated changes before merging, and avoid exposing unrelated secrets or wallet credentials during assessment or scaffolding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buddhasource/skills/crypto-payments-self-hosted-payram)
- [PayRam setup skill](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup)
- [PayRam helper MCP server](https://github.com/PayRam/payram-helper-mcp-server)
- [PayRam GitHub organization](https://github.com/PayRam)
- [PayRam website](https://payram.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce framework-specific payment routes, webhook handlers, environment templates, starter app scaffolding guidance, and MCP tool instructions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
