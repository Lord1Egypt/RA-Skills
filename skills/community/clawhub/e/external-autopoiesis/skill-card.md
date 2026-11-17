## Description:

Build persistent, evolving AI identity through external architecture around stateless LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crowloki](https://clawhub.ai/user/crowloki)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to design persistent identity, memory, correction, and evolution workflows around stateless LLM agents, including setup from scratch and maintenance across sessions or model swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may capture sensitive or regulated information.

Mitigation: Require explicit opt-in for what is stored, keep secrets and regulated personal data out of logs, and scope memory per user or project.

Risk: Instruction-bearing files can change agent behavior across sessions.

Mitigation: Review changes to identity, memory, and rule files before loading them into an agent session.

Risk: Recurring heartbeat or evolution jobs can create autonomous background activity.

Mitigation: Enable scheduled jobs only when the command, schedule, data access, logs, and removal procedure are clear.

Risk: Broad logging and self-modifying rules can make behavior harder to audit.

Mitigation: Keep logs scoped, append-only where practical, and review proposed rule changes before making them authoritative.

## Reference(s):

- [Autopoietic Evolution Protocol](references/evolution-protocol.md)
- [Ignition Guide](references/ignition-guide.md)
- [Technical Foundations](references/technical-foundations.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with file layout examples and optional shell command patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent memory files, cron or heartbeat schedules, and review steps; users should opt in before storing data or enabling background jobs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
