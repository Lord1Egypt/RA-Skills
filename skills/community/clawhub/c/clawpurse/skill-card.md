## Description:

ClawPurse is a local Neutaro chain wallet for managing NTMPI tokens, including balance checks, transfers, transaction history, staking, and allowlist enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhue-ai](https://clawhub.ai/user/mhue-ai)

### License/Terms of Use:

ISC

## Use Case:

Developers, automation operators, and agents use ClawPurse to operate a local Neutaro wallet, move NTMPI, inspect balances and transaction history, manage staking, and enforce destination allowlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can access a wallet that moves or stakes real NTMPI.

Mitigation: Use a dedicated wallet with limited funds, review transfer and staking commands before execution, and verify transaction hashes on-chain.

Risk: Wallet passwords or mnemonics could be exposed through unsafe operator handling.

Mitigation: Avoid passing secrets on the command line, keep mnemonic backups offline, use strong unique passwords, and restrict ~/.clawpurse file permissions.

Risk: Transfers to unintended destinations may be high impact.

Mitigation: Keep allowlist enforcement enabled, set per-destination limits, require memos where useful, and avoid allowlist overrides except for reviewed one-off transactions.

Risk: Production use depends on the package dependency set and local host security.

Mitigation: Audit and update dependencies before production deployment, and run ClawPurse only on trusted hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mhue-ai/skills/clawpurse)
- [Operator Guide](docs/OPERATOR-GUIDE.md)
- [Trust Model](docs/TRUST-MODEL.md)
- [Destination Allowlist](docs/ALLOWLIST.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Code]

**Output Format:** [CLI text output, JSON receipts and configuration files, and TypeScript API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet data is stored locally under ~/.clawpurse by default; transfer and staking operations may affect real NTMPI.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
