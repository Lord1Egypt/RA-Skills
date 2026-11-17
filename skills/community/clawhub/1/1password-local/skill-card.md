## Description:

Set up and use 1Password CLI (op) for installing the CLI, enabling desktop app integration, signing in, and reading, injecting, or running secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaozewen0519](https://clawhub.ai/user/zhaozewen0519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up authenticated 1Password CLI workflows and safely run common op commands for secrets access, injection, and account verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can print or persist real secrets, including unmasked command output and local secret files.

Mitigation: Avoid printing secret values, avoid --no-masking for real credentials, and prefer op run or op inject over writing secrets to disk.

Risk: Terminal captures and logs can expose credentials when commands are run against a secrets manager.

Mitigation: Use a fresh tmux session for op commands, verify the selected account before secret access, and keep captured output free of secret values.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [ClawHub skill page](https://clawhub.ai/zhaozewen0519/skills/1password-local)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal workflow steps for tmux-mediated 1Password CLI authentication and command execution.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
