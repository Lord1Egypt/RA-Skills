## Description:

Writes a structured handoff package when a local agent determines cloud Claude Code is needed, while leaving Claude Code execution under user control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlthorn](https://clawhub.ai/user/stephenlthorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to prepare a structured Claude Code handoff when local work reaches an escalation gate, build-failure limit, low-confidence review, context limit, or explicit user request. It captures task context, local findings, a proposed plan, and a ready-to-run command so the user can review the handoff before spending Claude Max quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated handoff files can contain task details, project context, file paths, build errors, and other sensitive development information.

Mitigation: Review the generated Markdown handoff for secrets, proprietary details, and unnecessary context before sending it to Claude Code.

Risk: Notification behavior can transmit handoff metadata when OPENCLAW_NOTIFY_ENDPOINT is configured.

Mitigation: Unset OPENCLAW_NOTIFY_ENDPOINT or restrict it to a trusted endpoint before using the skill in sensitive projects.

Risk: The ready-to-paste shell command includes the project path and should be treated carefully for projects with unusual or untrusted path names.

Mitigation: Inspect and edit the command before running it, especially when the project path was created from external input.

Risk: The skill writes local status and handoff-log files that may preserve metadata after the handoff is complete.

Mitigation: Review retention expectations for .openclaw-skills files and remove local handoff or log artifacts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stephenlthorn/skills/claude-handoff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown handoff file with a ready-to-paste shell command and short text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local handoff file under .openclaw-skills/handoffs and may write local notification and handoff-log files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
