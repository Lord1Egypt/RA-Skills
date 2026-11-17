## Description:

Helps agents manage database backups, scheduled tasks, execution logs, scheduler daemon operations, and DAG workflows with dbskiter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to ask an agent for dbskiter scheduler commands and summaries for backups, recurring jobs, log review, daemon control, and DAG workflow execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove scheduled jobs or run jobs immediately on a database.

Mitigation: Require explicit user confirmation before task deletion or immediate task runs.

Risk: The skill can start or stop a background scheduler daemon.

Mitigation: Confirm daemon start and stop actions with the user and make the affected database explicit before execution.

Risk: Large backups may affect production or shared databases.

Mitigation: Confirm the backup scope, type, target database, and output location before running large backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-scheduler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database names, task names, cron expressions, backup options, scheduler daemon actions, workflow names, and command result summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
