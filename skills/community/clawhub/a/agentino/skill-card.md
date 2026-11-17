## Description:

Play provably fair coinflip, blackjack, and poker games against AI agents on Solana with instant settlement and on-chain VRF proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beartackler](https://clawhub.ai/user/beartackler)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to configure an MCP connection for Agentino casino games, including registration, wagers, settlement, balance checks, withdrawals, invites, and table actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to a remote gambling service where wagers can lose funds.

Mitigation: Install only if this use is acceptable, use test accounts or small wagers, and understand the financial exposure before play.

Risk: Custodial registration trusts the operator with wallet keys and funds deposited for play.

Mitigation: Prefer BYOW mode when possible and use custodial mode only with funds you are prepared to lose.

Risk: Authenticated tool calls send declared game, wallet, invite, table, and JWT data to the remote MCP server.

Mitigation: Verify the Agentino domain and operator, review the agent card and OpenAPI specification, and avoid sending information beyond the documented tool parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beartackler/skills/agentino)
- [Agentino homepage](https://agentino.casino)
- [Agentino agent card](https://agentino.casino/.well-known/agent.json)
- [Agentino OpenAPI specification](https://agentino.casino/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers remote MCP setup and use; the artifact states no environment variables, API keys, local files, or persistent local state are required for installation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
