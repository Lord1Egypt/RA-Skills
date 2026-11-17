## Description:

Run long-running, multi-step work in OpenClaw with durable state, progress updates, smart recovery, verification before completion, and optional worker-lane coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wonko6x9](https://clawhub.ai/user/wonko6x9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to keep long-running OpenClaw work recoverable across resets by recording task state, checkpoints, progress, controls, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring status ticks can add persistent local execution through the current user's crontab.

Mitigation: Review before installing and do not run the cron --apply helper unless recurring ticks are intended and removal is understood.

Risk: Installer behavior can delete a chosen target directory.

Mitigation: Use the default install path only, and avoid custom --target paths unless the target has been reviewed and backed up.

Risk: Task goals, progress logs, and events can contain sensitive user-entered details.

Mitigation: Do not store secrets in task goals, progress logs, or events, and secure the local task-state storage.

Risk: Recovery can select the wrong task when more than one durable task exists.

Mitigation: Use explicit task IDs for recovery when multiple durable tasks are present.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [Durable Task Runner Schema](references/task-schema.md)
- [Control Levels](references/control-levels.md)
- [Subagent Return Protocol](references/subagent-return-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task-state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local task snapshots, event logs, and progress logs when used.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
