## Description:

BitNote provides decentralized encrypted memory for agents to preserve identity, secrets, and critical knowledge without relying on centralized infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockwellshah](https://clawhub.ai/user/rockwellshah)

### License/Terms of Use:

ISC

## Use Case:

Developers and agent operators use BitNote to read account mappings, write encrypted UI-compatible notes, preserve agent identity state, and generate recipient-bound share links. It is intended for workflows where persistent encrypted memory, retry-safe writes, and explicit operator approval for on-chain actions are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write and share workflows decrypt private-key material and can broadcast on-chain transactions.

Mitigation: Use read-only or dry-run modes first, require explicit human approval before non-dry-run writes, and test with a throwaway wallet that does not hold real funds.

Risk: Passphrases and decrypted secrets could be exposed through command arguments, logs, or committed profile data.

Mitigation: Provide secrets through protected environment variables or a secret manager, avoid passphrases in CLI arguments, keep profile JSON free of secrets, and redact sensitive output.

Risk: Incorrect request IDs or retry handling can create duplicate or unverifiable writes.

Mitigation: Use a stable request ID for each intended note and require TX_HASH, NOTE_INDEX, and READ_AFTER_WRITE_OK 1 before treating a write as successful.

## Reference(s):

- [BitNote Contracts](references/contracts.md)
- [BitNote Ops Runbook](references/ops.md)
- [BitNote Web App](https://app.bitnote.xyz)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deterministic request-id guidance, dry-run recommendations, and expected output markers for read, write, and share-link operations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
