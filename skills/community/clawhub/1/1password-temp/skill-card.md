## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, account selection, and secret access workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansolero](https://clawhub.ai/user/hansolero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up authenticated 1Password CLI workflows and safely run commands that read, inject, or pass secrets to local tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authenticated 1Password CLI session can expose passwords, OTPs, keys, or injected configuration in terminal output or chat.

Mitigation: Do not request secret values in chat or logs; prefer masked workflows and review command output before sharing it.

Risk: Examples that use `--no-masking`, `--out-file`, or generated config files can leave secrets visible or stored on disk.

Mitigation: Avoid unmasked output and secret files unless strict permissions, short retention, and cleanup are part of the workflow.

Risk: Letting an agent operate `op` means the agent may act within the permissions of the signed-in 1Password account.

Mitigation: Use only accounts and vaults appropriate for the task, verify the active account with `op whoami`, and stop if the requested access exceeds the intended scope.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/hansolero/skills/1password-temp)
- [ClawHub publisher profile](https://clawhub.ai/user/hansolero)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI binary `op`; Homebrew install metadata identifies formula `1password-cli`.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
