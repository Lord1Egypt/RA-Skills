## Description:

Decode and inspect X.509 SSL/TLS certificates. Use when the user asks to read a certificate, parse a PEM file, check certificate expiry, inspect a TLS cert, view Subject Alternative Names, or decode a .crt/.pem file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security engineers use this skill to inspect PEM or CRT certificates, fetch live TLS certificate details for a hostname, and summarize validity, issuer, SAN, key, signature, and expiry status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples can become unsafe if untrusted certificate text, file paths, or hostnames are substituted directly into shell commands.

Mitigation: Validate hostnames and paths, avoid shell interpolation for untrusted values, and pass certificate content to openssl through a temp file or safe process invocation.

Risk: The skill invokes openssl and may connect to live hostnames, which can expose the agent to untrusted inputs or unexpected network targets.

Mitigation: Install and run only where openssl execution and outbound TLS checks are acceptable, and review requested hosts before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with parsed certificate fields and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openssl; may fetch live TLS certificates for hostnames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
