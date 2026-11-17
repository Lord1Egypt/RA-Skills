## Description:

Anydef Enc provides local-only agent data encryption using an MK-to-KEK-to-DEK hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anydefai](https://clawhub.ai/user/anydefai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local browser-based encryption for selected agent data such as memory, history, assets, and audit data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports extractable key material held in memory without a clear lock mechanism.

Mitigation: Review before installing for strong same-page script compromise protection, clear in-memory key state on lock, logout, or session expiry, and prefer non-extractable operational keys where feasible.

Risk: The skill is zero-knowledge and does not provide password reset or passphrase recovery.

Mitigation: Use an operational process for passphrase retention and communicate that forgotten passphrases make encrypted data inaccessible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anydefai/skills/anydef-enc)
- [Local Encryption Architecture](references/full-implementation.md)
- [Storage Keys Dictionary](references/storage-keys.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [JavaScript modules and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser Web Crypto and window.storage; no external credentials are required.]

## Skill Version(s):

2.1.1 (source: release evidence and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
