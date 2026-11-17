## Description:

Access and manage Bitwarden passwords securely using the official bw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorha59](https://clawhub.ai/user/yorha59)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate Bitwarden CLI commands for retrieving vault item passwords, usernames, TOTP codes, item JSON, search results, and sync operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text advises storing BW_SESSION in a shell startup file, which can expose a vault session secret beyond the current shell.

Mitigation: Do not save BW_SESSION in shell profiles; unlock Bitwarden only for the active shell, unset BW_SESSION when finished, and lock the vault after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yorha59/skills/bitwarden-bw)
- [Publisher profile](https://clawhub.ai/user/yorha59)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Bitwarden CLI command guidance and expects the user environment to provide bw and a current BW_SESSION.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
