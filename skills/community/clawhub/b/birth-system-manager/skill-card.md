## Description:

Manage birth encoding, migration packing/unpacking, identity whoami, secure wallet decryption, and full family tree lineage tracking for OpenClaw agents with clone parent-child relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vg555558](https://clawhub.ai/user/vg555558)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create local birth identities, package and unpack migrations, initialize clones, inspect lineage, and manage wallet-backed identity verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet key material can be exposed when wallet decryption or migration features are used.

Mitigation: Use a contained environment with non-valuable test wallets unless the code is changed to avoid plaintext private keys and stop printing secrets.

Risk: Migration archives can include sensitive workspace data or overwrite trusted files during extraction.

Mitigation: Restrict package contents and validate migration archives before extraction.

## Reference(s):

- [Birth System Manager on ClawHub](https://clawhub.ai/vg555558/skills/birth-system-manager)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local identity files, encrypted wallet data, and migration archives.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
