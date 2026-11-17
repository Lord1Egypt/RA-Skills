## Description:

Always-on self-awareness framework for OpenClaw agents that provides runtime, memory, storage, context-health, and failure-handling guidance for meta questions, self-checks, and drift prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inxan3](https://clawhub.ai/user/inxan3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep an OpenClaw agent grounded in platform behavior, memory and storage conventions, failure handling, and self-check routines. It supports answering meta questions, diagnosing unexpected behavior, and running periodic or on-demand self-checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to create a recurring weekly self-check schedule without clear user opt-in.

Mitigation: Require explicit user approval before enabling any cron schedule, and confirm the schedule and timezone before creation.

Risk: Self-checks can involve broad workspace, memory, cron, and storage review with persistent drift-log entries.

Mitigation: Limit logged content to operational findings, avoid secrets or sensitive user data, and review where the drift log is stored.

Risk: The artifact includes secret-storage guidance that may be unsafe if memory files are indexed, logged, or included in model context.

Mitigation: Use platform-protected secret storage or environment configuration, and exclude any secret files from indexing, logs, and model context.

## Reference(s):

- [Delphi Skill Page](https://clawhub.ai/inxan3/skills/delphi)
- [Platform Truths](references/platform-truths.md)
- [Storage Conventions](references/storage-conventions.md)
- [Failure Protocol](references/failure-protocol.md)
- [Drift Catalog](references/drift-catalog.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, shell command examples, JSON cron configuration, and self-check report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt persistent drift-log entries and scheduled self-check setup when followed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
