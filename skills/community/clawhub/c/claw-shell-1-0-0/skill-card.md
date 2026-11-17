## Description:

Runs shell commands inside a dedicated tmux session named claw, captures pane output, and asks for confirmation before potentially destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlshiny](https://clawhub.ai/user/zlshiny)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run shell commands through a dedicated tmux session and return captured terminal output to the agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad shell access through a persistent tmux session.

Mitigation: Install only in a tightly sandboxed environment with a runtime account that cannot access sensitive files, credentials, or important system state.

Risk: Dangerous-command detection is a weak safety boundary.

Mitigation: Require explicit human approval for destructive or privileged commands and do not rely on the warning as the sole control.

Risk: Captured tmux output and long-lived sessions can expose or retain sensitive terminal state.

Mitigation: Avoid use in environments with long-lived sensitive sessions and clear or isolate the tmux session after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlshiny/skills/claw-shell-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/zlshiny)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON object containing the command and captured terminal output, or an error object for blocked dangerous commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a tmux session named claw; dangerous-command checks are advisory and require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
