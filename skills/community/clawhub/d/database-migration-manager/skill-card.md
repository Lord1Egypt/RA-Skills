## Description: <br>
Database migration manager that detects ORM and migration tools, generates migrations, handles rollbacks, creates seed scripts, diffs schemas between environments, backs up databases, and supports zero-downtime patterns for Prisma, Drizzle, Knex, TypeORM, Alembic, Django, raw SQL, Postgres, MySQL, and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, generate, review, run, roll back, seed, diff, and back up database migrations across common ORM and SQL workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration, rollback, DROP, DELETE, push, reset, restore, and backup commands can change or destroy real database state. <br>
Mitigation: Verify the target environment and database URL, review generated SQL or migration files, and require explicit confirmation before allowing high-impact commands. <br>
Risk: Production migrations can fail or lock tables if applied without preparation. <br>
Mitigation: Confirm a fresh backup exists, test changes against staging or a production-like copy, and use zero-downtime patterns for breaking schema changes. <br>
Risk: Environment files may contain database credentials. <br>
Mitigation: Use the project's existing configuration only and avoid logging or displaying connection strings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/llcsamih/database-migration-manager) <br>
- [Publisher profile](https://clawhub.ai/user/llcsamih) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL, code, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose migration files, rollback steps, backup commands, seed scripts, schema diffs, and production safety checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
