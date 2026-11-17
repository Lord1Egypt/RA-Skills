## Description:

Agent Task Logger records agent task starts, command execution, status updates, errors, and live log viewing in a Tomcat-style local task log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gerald-luo](https://clawhub.ai/user/gerald-luo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to initialize a workspace task log, record task progress and command activity, inspect task status, and follow the log during agent-driven work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command strings, project paths, errors, or other sensitive task details may be written to persistent local log files.

Mitigation: Avoid logging tokens, credentials, secrets, and sensitive paths; review log contents before sharing or archiving them.

Risk: The logger has weak destination controls and may write to an unintended workspace or log filename.

Mitigation: Use a trusted workspace, set the workspace and log filename deliberately, and verify the resolved log path before recording tasks.

Risk: Local task logs can grow over time and retain operational history longer than intended.

Mitigation: Apply log retention or rotation and delete logs that are no longer needed.

## Reference(s):

- [Agent Task Logger on ClawHub](https://clawhub.ai/gerald-luo/skills/agent-task-logger)
- [ClawHub](https://clawhub.ai)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Bash log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local task logs in the selected workspace log directory.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
