## Description:

Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daggerkun007](https://clawhub.ai/user/daggerkun007)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and verify the 1Password CLI, enable desktop app integration, authenticate accounts, and run secret read, inject, and command workflows through op.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may print decrypted secrets, disable masking, or write decrypted secrets to local files.

Mitigation: Avoid those examples unless there is a specific need and logs, file permissions, cleanup, and credential rotation risk are controlled.

Risk: An authenticated 1Password CLI session can access sensitive vault data.

Mitigation: Use the skill only when intentionally operating an authenticated op session, verify the account with op whoami, and prefer op run or op inject over persisting secrets to disk.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/daggerkun007/skills/1password-1-0-1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI binary op; authenticated op commands are expected to run in a dedicated tmux session.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
