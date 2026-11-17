## Description:

A2A Gateway provides an OpenClaw agent collaboration bus for registering agent cards, routing delegated tasks, tracking task state, reviewing audit trails, and checking agent health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage an OpenClaw multi-agent network, including agent discovery, capability-based routing, delegated task lifecycle tracking, collaboration audit logs, and health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags under-scoped persistent cron execution.

Mitigation: Review scripts/setup-cron.sh before use and run it only when the referenced health.py path and twice-daily user crontab execution are intended.

Risk: The release security guidance warns that local collaboration logs and pending spawn files may contain sensitive task content.

Mitigation: Avoid placing secrets in task descriptions, task results, errors, or pending spawn files, and review local log retention before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/a2a-gateway)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON or JSONL registry, task, audit, performance, knowledge, and cron-related files when the bundled scripts are run.]

## Skill Version(s):

1.0.5 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
