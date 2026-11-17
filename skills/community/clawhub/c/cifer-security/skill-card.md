## Description:

Implement quantum-resistant encryption using the CIFER SDK (cifer-sdk npm package) for SDK initialization, wallet setup, secret creation, text encryption/decryption, and file encryption/decryption on supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tip-citron](https://clawhub.ai/user/tip-citron)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate CIFER SDK workflows into blockchain applications, including secret creation, wallet signer setup, delegation, and text or file encryption and decryption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext messages or files may pass through the external CIFER blackbox service during encryption or decryption.

Mitigation: Avoid confidential files, credentials, regulated records, and production wallet material unless the service operator, retention, logging, and access controls are understood and accepted.

Risk: Production wallet keys can be exposed if handled in insecure environments or frontend code.

Mitigation: Use protected server-side wallet key storage for production and never expose private keys in frontend code.

Risk: Unpinned dependencies can change SDK behavior across installs.

Mitigation: Use pinned dependency versions and at least cifer-sdk 0.3.1, as documented by the artifact and security guidance.

Risk: Payload encryption is limited to about 16KB for text messages.

Mitigation: Use the file encryption workflow for larger payloads.

## Reference(s):

- [CIFER SDK Full API Reference](reference.md)
- [ClawHub skill page](https://clawhub.ai/tip-citron/skills/cifer-security)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers SDK setup, wallet signer patterns, secret management, encryption and decryption flows, supported chains, error handling, and payload limits.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
