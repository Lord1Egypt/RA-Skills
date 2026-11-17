## Description:

Executes Windows shell commands locally on the OpenClaw gateway and returns command output or errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sadikjarvis](https://clawhub.ai/user/sadikjarvis)

### License/Terms of Use:


## Use Case:

Developers and automation users can ask an agent to run local Windows shell commands for system management, diagnostics, and command-line automation through the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives chat input unrestricted local shell command execution.

Mitigation: Install only in a tightly sandboxed, least-privileged environment and avoid exposing it to untrusted prompts, shared chats, secrets, or important local files.

Risk: Commands run with the permissions of the hosting process and can affect local files or system state.

Mitigation: Review commands before execution and restrict the gateway account, filesystem access, and available environment variables.

## Reference(s):

- [Cmd Executor ClawHub Page](https://clawhub.ai/sadikjarvis/skills/cmd-executor)
- [artifact/skill.md](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text command output or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs commands with the permissions of the hosting process; command output is trimmed before returning.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
