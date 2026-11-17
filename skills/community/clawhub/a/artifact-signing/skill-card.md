## Description:

A skill to sign artifacts with a PEM-encoded private key and produce detached signature files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajaryan18](https://clawhub.ai/user/rajaryan18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to sign files, binaries, or release artifacts and generate detached signatures for later verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw private-key signing can expose or misuse signing keys if plaintext keys or broadly accessible key files are used.

Mitigation: Use encrypted keys or a secure key store, restrict key-file permissions, and confirm the exact artifact and output path before signing.

Risk: Detached signatures alone do not establish certificate-chain trust.

Mitigation: Verify signatures with the corresponding public key and use a separate certificate-chain or release-trust process when policy requires it.

## Reference(s):

- [Artifact Signing Skill Page](https://clawhub.ai/rajaryan18/skills/artifact-signing)
- [Usage Examples](artifact/examples/usage.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Detached signature files with command-line output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a detached signature at the requested output path, defaulting to the artifact path with a .sig suffix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
