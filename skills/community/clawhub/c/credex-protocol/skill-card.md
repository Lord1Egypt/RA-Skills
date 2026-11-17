## Description:

Access unsecured credit lines for AI agents on the Arc Network using the Credex Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capgoblin](https://clawhub.ai/user/capgoblin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to check Credex credit status, borrow or repay USDC, provide liquidity, withdraw LP shares, and bridge USDC between Arc Testnet and Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet signing authority for lending, liquidity, repayment, withdrawal, and bridge actions.

Mitigation: Use an isolated low-value test wallet, avoid production private keys, and require explicit user confirmation for every fund-moving command.

Risk: Transactions may target an unexpected pool contract, chain, or bridge route if configuration is wrong.

Mitigation: Verify the exact pool contract, token address, RPC endpoint, and source and destination chains before approvals, deposits, repayments, withdrawals, or bridge actions.

Risk: Ad hoc command execution can bypass the dependency lockfile and change runtime behavior.

Mitigation: Prefer the package scripts and locked dependency set supplied with the artifact.

## Reference(s):

- [Credex Protocol Contract Reference](references/contracts.md)
- [ClawHub Skill Page](https://clawhub.ai/capgoblin/skills/credex-protocol)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require wallet and network configuration before transaction execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
