## Description:

Provides AgentPMT-hosted remote cryptography actions for generating secure random values, hashing, HMACs, digital signatures, and AES-256-GCM encryption or decryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call AgentPMT-hosted cryptographic utilities for secure token generation, checksums, HMAC validation, signatures, and AES-256-GCM encryption workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote cryptography calls can expose plaintext, private keys, HMAC secrets, AES keys, credentials, or private file contents to AgentPMT.

Mitigation: Use the skill only when AgentPMT is explicitly trusted for the exact data being processed; avoid production secrets and prefer local cryptographic tools or KMS/HSM key references for sensitive work.

Risk: Live remote instructions and setup commands can change after installation.

Mitigation: Independently review live instructions before production use and pin or replace setup commands with reviewed, controlled installation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/encrytion-decryption-toolkit)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit)
- [Generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and schema references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool responses are JSON outputs from the selected AgentPMT action.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
