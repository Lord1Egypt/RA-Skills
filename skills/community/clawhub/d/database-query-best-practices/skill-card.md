## Description:

Helps agents prevent Railway PostgreSQL connection pool exhaustion by checking connection usage, closing database connections promptly, using short-lived queries, and preferring Railway CLI for ad hoc SQL when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when querying Railway PostgreSQL databases from local scripts, diagnosing connection-pool exhaustion, or preparing safer short-lived database queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad process and database session termination examples that can stop unrelated local processes or interrupt production database sessions.

Mitigation: Require scoped, preview-first procedures and explicit approval before running commands such as pkill -9 or pg_terminate_backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/database-query-best-practices)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
