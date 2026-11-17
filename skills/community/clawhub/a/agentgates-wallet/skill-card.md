## Description:

Pair an Agentgates wallet over MCP (OAuth) and act under owner-approved grants: read balances, propose sends, swaps and earn moves; the owner approves every money move.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect an Agentgates wallet through OAuth, read balances and history, and propose sends, swaps, or earn moves for the owner to approve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet access depends on the OAuth permissions granted to the connected wallet.

Mitigation: Review the wallet and OAuth permissions before connecting.

Risk: The external service implementation and credential storage were not verified, and the CLI source has not been verified by this review.

Mitigation: Verify the CLI source before installing it and check the details of every browser approval.

## Reference(s):

- [Agentgates agent authentication documentation](https://agentgates.ai/auth.md)
- [Agentgates MCP endpoint](https://mcp.agentgates.ai/api/mcp)
- [ClawHub skill page](https://clawhub.ai/agentgates/skills/agentgates-wallet)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown instructions with inline shell commands and endpoint/scopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
