## Description: <br>
Use when designing database schemas, writing migrations, optimizing SQL queries, fixing N+1 problems, creating indexes, setting up PostgreSQL, configuring EF Core, implementing caching, partitioning tables, or any database performance question. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgarrison929](https://clawhub.ai/user/jgarrison929) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for database schema design, PostgreSQL query optimization, migration planning, EF Core migration workflows, caching strategies, partitioning, and performance troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or migration guidance could change or remove production data if applied without review. <br>
Mitigation: Review generated SQL, test migrations in a non-production environment, and confirm rollback procedures before applying changes. <br>
Risk: Audit logging examples may copy sensitive fields into audit tables. <br>
Mitigation: Filter or redact sensitive fields before enabling audit triggers or storing old and new row values. <br>
Risk: Caching and materialized-view guidance can serve stale data if invalidation or refresh timing is wrong. <br>
Mitigation: Define cache invalidation rules, refresh schedules, and monitoring before using generated caching or materialized-view patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jgarrison929/database-operations) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with SQL, shell, C#, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; generated database changes should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
