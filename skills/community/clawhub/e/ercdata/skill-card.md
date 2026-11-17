## Description:

Store, verify, and manage AI data on the Ethereum blockchain (Base network) using the ERCData standard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xreisearch](https://clawhub.ai/user/0xreisearch)

### License/Terms of Use:


## Use Case:

Developers and agent builders use ERCData to store blockchain-backed fingerprints, audit trails, access-controlled records, and verification data for AI memory, identity, outputs, and model provenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Data written to Base mainnet can be permanent and publicly observable, including raw transaction calldata even when the skill uses its private access-control mode.

Mitigation: Store only hashes or pre-encrypted content, and avoid placing sensitive plaintext or secrets in on-chain data or metadata.

Risk: Write and verification commands require a funded wallet and can incur Base mainnet transaction costs.

Mitigation: Use a dedicated minimally funded wallet and review the target contract, RPC endpoint, and transaction details before submitting transactions.

Risk: Passing private keys with command-line flags can expose credentials through shell history or process inspection.

Mitigation: Prefer environment-based or external secret management and avoid using the `--key` flag with long-lived wallets.

## Reference(s):

- [ERCData API Reference](artifact/references/api.md)
- [ClawHub ERCData Skill Page](https://clawhub.ai/0xreisearch/skills/ercdata)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Base mainnet, an ERCData contract address, RPC configuration, wallet credentials, and role-based permissions for write and verification operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
