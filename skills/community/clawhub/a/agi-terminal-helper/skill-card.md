## Description:

A practical runbook for using OpenClaw exec safely (sandbox-first, explicit confirmations, and debugging playbooks).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwujijay](https://clawhub.ai/user/liuwujijay)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide an assistant's terminal work with safer command planning, sandbox-first exploration, explicit confirmation for risky actions, and debugging playbooks for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal guidance can still influence command selection, and a proposed command may be inappropriate for the user's workspace or intent.

Mitigation: Review each proposed command against its stated purpose, working directory, and expected file effects before execution.

Risk: Examples involving destructive, privileged, credential-related, or system-level operations could cause harm if followed without confirmation.

Mitigation: Require explicit user confirmation for risky operations and avoid pasting secrets or running remote install scripts without review.

Risk: Platform-specific troubleshooting, especially macOS permission guidance, may not match the local OpenClaw environment.

Mitigation: Validate local tool availability, permissions, and sandbox environment settings before applying platform-specific playbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwujijay/skills/agi-terminal-helper)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
