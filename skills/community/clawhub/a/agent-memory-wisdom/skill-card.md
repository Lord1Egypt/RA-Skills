## Description:

brain 大脑 helps OpenClaw agents route tasks, assess confidence, maintain lightweight session memory, write checkpoints, and reuse experience capsules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[384961890-ui](https://clawhub.ai/user/384961890-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add a lightweight memory and task-routing workflow around agent sessions, including confidence-based routing, checkpointing, subagent budgeting, watchdog retries, and reusable experience capsules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task history and local memory may be stored and later reused in session context.

Mitigation: Avoid putting secrets in task descriptions or commands, and clear memory and log files regularly.

Risk: bootstrapExtraFiles can inject local memory files into future sessions.

Mitigation: Review the configured files before enabling bootstrapExtraFiles, or disable that setting in sensitive workspaces.

Risk: The watchdog utility exposes broad shell and subagent execution modes.

Mitigation: Review, remove, or restrict subagent-watchdog.js exec mode before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/384961890-ui/skills/agent-memory-wisdom)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON routing decisions and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When scripts are run, they may create or update local checkpoint, routing-log, memory, and capsule files; the user edition documents a 3-fragment memory pool and a 2-concurrent-subagent limit.]

## Skill Version(s):

1.1.7 (source: server release metadata; artifact frontmatter reports 1.1.7-user)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
