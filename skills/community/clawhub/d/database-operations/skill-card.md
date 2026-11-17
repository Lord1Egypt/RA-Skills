## Description:

Use when designing database schemas, writing migrations, optimizing SQL queries, fixing N+1 problems, creating indexes, setting up PostgreSQL, configuring EF Core, implementing caching, partitioning tables, or any database performance question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgarrison929](https://clawhub.ai/user/jgarrison929)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design database schemas, plan migrations, tune PostgreSQL queries, address N+1 problems, choose indexes, configure EF Core migrations, and apply caching or partitioning patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample audit trigger can copy password hashes, tokens, secrets, MFA data, or personal data into audit logs.

Mitigation: Use explicit allowlists or field exclusions before adapting audit logging patterns to sensitive tables.

Risk: Migration and EF database update examples can change production databases if used without environment checks.

Mitigation: Confirm the target environment, backups, generated SQL, staging results, and rollback plan before applying database-changing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jgarrison929/skills/database-operations)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with SQL, C#, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory patterns and command templates that should be reviewed before use against production databases.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
