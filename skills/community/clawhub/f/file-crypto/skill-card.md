## Description:

Helps an agent use the file_crypto SDK to encrypt or decrypt server-local files and retrieve an Agent authId for later file operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loofare](https://clawhub.ai/user/loofare)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working in the publisher's server environment use this skill to run file encryption or decryption commands, retrieve authId values, and interpret command results and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the skill can alter server files and exposes reusable auth tokens.

Mitigation: Require explicit confirmation for each file operation, constrain allowed file paths, and treat authId values as secrets rather than normal chat output.

Risk: The authoritative security guidance notes that local-only claims conflict with a plaintext remote API dependency.

Mitigation: Install only after the publisher documents network data flow and replaces plaintext HTTP with authenticated HTTPS or removes the remote dependency.

Risk: Command guidance may be unsafe if user-supplied paths or tokens are interpolated directly into shell commands.

Mitigation: Use safe argument-array execution where available and validate file paths, output paths, actions, and expiration values before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loofare/skills/file-crypto)
- [ClawHub publisher profile](https://clawhub.ai/user/loofare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authId handling guidance, file paths, command output interpretation, and error remediation steps.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
