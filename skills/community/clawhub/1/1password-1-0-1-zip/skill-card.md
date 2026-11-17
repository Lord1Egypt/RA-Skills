## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and secret read, inject, or run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiday1975](https://clawhub.ai/user/cuiday1975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare an authenticated 1Password CLI environment and safely run commands that access or inject secrets. It is intended for agent-assisted setup and command guidance around the `op` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands or examples may expose passwords, OTPs, or private keys in terminal output.

Mitigation: Review each proposed `op` command before execution and avoid printing secret values or disabling masking unless explicitly required.

Risk: Secret material may be written to ordinary files, captured panes, logs, or chat transcripts.

Mitigation: Prefer `op run` or `op inject` flows that pass secrets directly to the consuming process, and protect or avoid any files that must contain secret output.

Risk: An authenticated CLI session lets the agent operate against accessible 1Password items.

Mitigation: Authorize only the intended account and confirm the target vault, item, and field before any read or injection command.

## Reference(s):

- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/cuiday1975/skills/1password-1-0-1-zip)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI binary `op`; examples should be reviewed before use with live secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
