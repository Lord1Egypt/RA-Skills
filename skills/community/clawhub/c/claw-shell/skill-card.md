## Description:

Runs shell commands in a dedicated tmux session named claw, captures pane output, and returns it to the agent with basic checks for destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaginelogo](https://clawhub.ai/user/imaginelogo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when they intentionally want an agent to run shell commands through a persistent tmux session and inspect the resulting output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a raw shell-command tool that may run commands with the local account's permissions.

Mitigation: Install only when agent-facing shell access is intentional, avoid use with untrusted prompts or content, and review commands before execution.

Risk: The supplied security evidence says the tmux isolation and risky-command confirmation controls are not reliable.

Mitigation: Prefer a version that uses argument-array process execution and real per-command approval for destructive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaginelogo/skills/claw-shell)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text response containing the submitted command, captured shell output, or safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is captured from the latest tmux pane contents for the claw session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
