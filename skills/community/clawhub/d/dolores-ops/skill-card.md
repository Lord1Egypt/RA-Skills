## Description:

OpenClaw 运维工具 - 负责 AI 助手自身的日常运维工作，包括健康检查、Memory 同步、目录清理、日志管理、定时任务管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[milesnee](https://clawhub.ai/user/milesnee)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and developers use this skill to have an OpenClaw assistant perform routine self-maintenance: health checks, memory synchronization, workspace cleanup, log review, and cron task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read past conversations and persist long-term memory, which can expose or retain sensitive information.

Mitigation: Review memory entries before they are written and avoid storing secrets or sensitive conversation details.

Risk: The skill may clean workspace files, including deletion of files selected during maintenance.

Mitigation: Require explicit review of exact deletion paths before cleanup and preserve protected directories, memory files, and user files.

Risk: The skill may create recurring cron or heartbeat tasks.

Mitigation: Review task names, schedules, and actions before enabling recurring execution, and record the created task ID.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown status reports with optional shell commands and heartbeat or cron configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational checklists, memory summaries, cleanup plans, log review summaries, and recurring task setup guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
