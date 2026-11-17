## Description:

Multi-agent AI coding swarm orchestration that plans parallel tasks, spawns Claude, Codex, and Gemini agents in tmux sessions with git worktrees, and supports automated review, branch integration, and Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkbag](https://clawhub.ai/user/linkbag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to split coding work into parallel agent tasks, supervise human approval before spawning workers, and coordinate review, integration, logging, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended agents and scripts can modify, commit, push, and merge project code.

Mitigation: Run the skill only in disposable or tightly scoped repositories, keep protected branches unavailable to the scripts, and require human review before any changes reach production branches.

Risk: Permission-bypass flags and approval bypasses can grant agents broad shell authority.

Mitigation: Remove bypass flags before operational use and run agents with least-privilege credentials in a sandboxed environment.

Risk: Telegram notifications and persisted work logs may disclose project details.

Mitigation: Use non-sensitive test projects by default, limit notification content, and keep logs and notification targets access-controlled.

## Reference(s):

- [Role Definition](references/ROLE.md)
- [Tools Notes](references/TOOLS.md)
- [Heartbeat Checks](references/HEARTBEAT.md)
- [Duty Table Template](references/duty-table-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and task prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration guidance and command/configuration artifacts for agent execution; shell scripts may create worktrees, branches, logs, notifications, commits, and pushes when run by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
