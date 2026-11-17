## Description:

Catfee SSH helps an agent connect to remote servers over password-based SSH to run commands, inspect configuration, diagnose issues, and perform file operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent connect to a remote server with user-provided SSH credentials for diagnostics, configuration inspection, log review, and file or service operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires SSH credentials and can enable remote administrative command execution.

Mitigation: Use least-privilege accounts, avoid root where possible, and explicitly approve restart, reload, file modification, sudo, or other administrative commands.

Risk: Password-based SSH and automatic host acceptance can weaken authentication and host verification safeguards.

Mitigation: Prefer SSH keys or a secure secret mechanism, verify server host fingerprints before connecting, and avoid storing or exposing passwords in prompts, logs, or command output.

Risk: The skill can automatically install the latest Posh-SSH module.

Mitigation: Preinstall and review a pinned Posh-SSH version before use instead of relying on automatic latest-version installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glory904649854/skills/catfee-ssh)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote command suggestions and operational steps that require user review before execution.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
