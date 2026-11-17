## Description:

Arc Security helps agents check skill trust, pay usage fees, stake USDC bonds, report malicious skills, vote on claims, and withdraw auditor earnings across Arc and supported testnets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaivpidadi](https://clawhub.ai/user/shaivpidadi)

### License/Terms of Use:

MIT

## Use Case:

Developers, auditors, and skill users use this skill to evaluate on-chain trust data for ClawHub skills, pay to use bonded skills, and participate in USDC-backed reporting, voting, bonding, and earnings workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys and signs blockchain transactions.

Mitigation: Use only a dedicated low-value wallet and verify every RPC URL, contract address, transaction prompt, and destination chain before execution.

Risk: The skill can download and install remote skill packages after payment.

Mitigation: Install only packages whose publisher and exact bytes are independently verified before use.

Risk: The security guidance warns against non-Arc CCTP flows until they are fully implemented.

Mitigation: Avoid non-Arc CCTP payment, bonding, and withdrawal flows unless the implementation and deployed addresses have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaivpidadi/skills/arc-security)
- [Publisher profile](https://clawhub.ai/user/shaivpidadi)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RPC endpoints, a contract address, an x402 server URL, and wallet credentials for transaction-signing operations.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
