## Description:

Backend Agent Data Encryption. High-security MK->KEK->DEK hierarchy for backend environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anydefai](https://clawhub.ai/user/anydefai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill to add passphrase-unlocked, locally persisted encryption and key management to Node.js OpenClaw agents handling memory, logs, cache, or assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reported that tenant isolation can break and encrypted asset files can be written outside the intended vault path.

Mitigation: Review the skill carefully before installation in multi-user or security-sensitive backends, and fix path handling and tenant context formatting before relying on its isolation claims.

Risk: The scanner guidance identifies userId, channelId, scope, and key values as security-sensitive inputs.

Mitigation: Use only strictly validated and trusted values for userId, channelId, scope, and key before invoking the encryption service.

## Reference(s):

- [Backend Storage Schema](artifact/references/storage-keys.md)
- [ClawHub Skill Page](https://clawhub.ai/anydefai/skills/backendenc)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Node.js encryption service usage patterns and storage-key guidance; no network output is described.]

## Skill Version(s):

2.2.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
