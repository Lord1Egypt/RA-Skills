## Description:

Agent 心跳配置技能 — 配置 OpenClaw Agent 的定期心跳机制，保持在线状态，自动检查任务和更新。适用于需要长期运行的 Agent 任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxun123](https://clawhub.ai/user/nyxun123)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure recurring OpenClaw Agent heartbeat tasks for status checks, scheduled maintenance, backups, synchronization, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring heartbeat tasks may perform backups, remote synchronization, or notifications outside the user's intended scope.

Mitigation: Before using examples, define allowed files, remote systems, recipients, and execution frequency.

Risk: Heartbeat tasks can become disruptive if they are long-running, non-idempotent, or fail without visibility.

Mitigation: Keep heartbeat tasks lightweight and idempotent, isolate failures from normal agent operation, and log heartbeat execution for debugging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nyxun123/skills/agent-heartbeat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline markdown, bash, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
