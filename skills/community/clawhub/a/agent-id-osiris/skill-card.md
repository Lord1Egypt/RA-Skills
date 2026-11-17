## Description:

Cryptographic identity for AI agents - sign and verify agent messages

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to generate agent key pairs, sign and verify messages, derive persistent agent IDs, and produce signed Agent Cards for agent interoperability workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated private keys can be long-lived or insufficiently protected.

Mitigation: Use password-protected keys, restrict key-directory permissions, back up keys securely, and never share private keys.

Risk: Command-line passwords can expose real secrets through process listings, logs, or shell history.

Mitigation: Avoid command-line passwords for real secrets; use safer secret input or environment handling outside test use.

Risk: Unsafe agent names can cause key files to be written outside the intended keys directory.

Mitigation: Run the skill in an isolated, non-privileged environment and use simple agent names without slashes or parent-directory components.

## Reference(s):

- [Agent Identity on ClawHub](https://clawhub.ai/nantes/skills/agent-id-osiris)
- [nantes Publisher Profile](https://clawhub.ai/user/nantes)
- [Metadata Homepage](https://github.com)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with CLI command examples; runtime output is plaintext for key and signature operations and JSON for signed Agent Cards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can write PEM key files under a local keys directory and requires Python with the cryptography package.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
