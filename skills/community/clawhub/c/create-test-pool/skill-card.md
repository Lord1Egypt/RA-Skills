## Description:

Deploy a custom Uniswap pool on the local testnet with configurable parameters to test agent behavior under controlled conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create local Uniswap V2 or V3 test pools with controlled tokens, fees, prices, liquidity, and tick ranges for agent and strategy testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install targets can change between review and installation.

Mitigation: Install a pinned ClawHub package version or a GitHub commit SHA before use.

Risk: The skill can change pool state and fund accounts while creating local test pools.

Mitigation: Use it only against a local testnet or fork where those state changes are intended.

Risk: Pool deployment depends on a running local testnet and available Uniswap contracts.

Mitigation: Confirm the local testnet is running and verify pool details after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/create-test-pool)
- [Publisher profile](https://clawhub.ai/user/wpank)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with pool details, verification results, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Uniswap MCP tool calls to deploy pools, fund local test accounts, search tokens, and query pool information.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
