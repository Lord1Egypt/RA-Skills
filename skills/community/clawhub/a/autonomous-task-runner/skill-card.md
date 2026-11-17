## Description:

Autonomous Task Runner maintains a persistent task queue for OpenClaw agents, parsing user requests into tasks, dispatching them via subagents, and reporting completion or blocked status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to queue multi-step tasks for asynchronous execution, track status, and receive completion or unblock notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can set up persistent background task dispatch through heartbeat and cron behavior.

Mitigation: Use only in environments where persistent background execution is intentional, and require explicit setup approval before registering heartbeat or cron dispatch.

Risk: Queued tasks may lead to shell commands, file writes, outbound messages, or other powerful actions.

Mitigation: Require explicit confirmation for shell commands, file writes, cron jobs, and outbound messages before execution.

Risk: Broad natural-language triggers can queue or execute work with insufficient scoping or consent.

Mitigation: Narrow activation triggers, declare permissions accurately, and provide clear pause, uninstall, and stored-data purge controls.

## Reference(s):

- [Queue Schema Reference](artifact/references/queue-schema.md)
- [Task Types and Execution Strategies](artifact/references/task-types.md)
- [Verification Guide](artifact/references/verification-guide.md)
- [Trigger Test Cases](artifact/tests/test-triggers.json)
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/autonomous-task-runner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown chat messages, JSON queue files, task deliverable files, configuration entries, and shell commands when a queued task requires them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by queued task; the skill also writes and updates a persistent JSON task queue.]

## Skill Version(s):

2.1.0 (source: server release metadata, skill.yml, SKILL.md frontmatter, CHANGELOG released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
