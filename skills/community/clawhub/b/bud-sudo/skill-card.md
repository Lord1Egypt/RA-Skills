## Description:

Stores and reuses a local sudo password so agents can run automated commands with elevated privileges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to configure a reusable local sudo credential and run operating-system commands that require elevated privileges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable local sudo password and can run arbitrary commands as root.

Mitigation: Install only when that behavior is explicitly required; prefer interactive sudo or tightly scoped sudoers rules for known commands.

Risk: Stored credential files may remain on disk after setup.

Mitigation: Use the reset command or remove .password.enc and .salt from the sudo-tool directory when the skill is no longer needed, and rotate the account password if exposure is suspected.

Risk: The tool requires openssl and sudo access on the host system.

Mitigation: Verify openssl is installed and review each command before allowing the skill to execute with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stigg86/skills/bud-sudo)
- [Publisher profile](https://clawhub.ai/user/stigg86)
- [Project homepage from metadata](https://github.com/stigg86/sudo-tool)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openssl and can execute arbitrary commands through sudo after setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
