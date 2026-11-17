## Description:

Enable quantum-resistant encryption and secret management for blockchain applications with post-quantum ML-KEM-768 key encapsulation and multi-chain support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohsinriaz17](https://clawhub.ai/user/mohsinriaz17)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add CIFER SDK encryption, secret management, file encryption, and on-chain encrypted data reference workflows to blockchain applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive plaintext, files, and signer-backed operations may be routed through the remote CIFER Blackbox service.

Mitigation: Do not send regulated, proprietary, credential-bearing, or highly sensitive data through the service unless that remote processing is explicitly accepted.

Risk: Examples include wallet signing and server-side private-key integrations that can affect user assets or authorization.

Mitigation: Use dedicated low-privilege keys or managed signers, pin and review SDK versions, and require explicit user approval before uploading files or signing messages.

## Reference(s):

- [Cifer SDK ClawHub page](https://clawhub.ai/mohsinriaz17/skills/cifer-sdk)
- [Cifer SDK npm package](https://www.npmjs.com/package/cifer-sdk)
- [Cifer SDK GitHub repository](https://github.com/cifer-security/cifer-sdk)
- [CIFER Blackbox API](https://blackbox.cifer.network)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation examples for SDK initialization, wallet integration, encryption, decryption, file jobs, transaction intents, and error handling.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
