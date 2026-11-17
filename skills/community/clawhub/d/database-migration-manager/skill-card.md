## Description:

Database Migration Manager helps developers detect database migration tooling, generate and run migrations, plan rollbacks, create seed scripts, compare schemas, back up databases, and use zero-downtime patterns across common ORMs and SQL databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage database schema changes, migration generation and execution, rollbacks, seed data, schema diffs, backups, and production-oriented zero-downtime migration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect database environment files and use sensitive database credentials while preparing or running migrations.

Mitigation: Use only existing project configuration, avoid displaying connection strings, and require operator review before any database action.

Risk: The skill may run unpinned local migration tools such as Prisma, Drizzle, Knex, TypeORM, Alembic, Django, psql, mysql, sqlite3, or migra.

Mitigation: Prefer projects where migration tools are already installed as pinned, lockfile-controlled dependencies before executing generated commands.

Risk: Migration, rollback, DROP, DELETE, and schema push commands can cause data loss or production outages.

Mitigation: Require explicit confirmation for destructive or production actions, review generated SQL, test on staging data, and create backups before production migrations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, SQL snippets, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include high-impact migration, rollback, backup, and schema-diff steps; production and destructive actions require explicit confirmation and backups.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
