## Description: <br>
Database Operations helps developers design schemas, write migrations, optimize SQL queries, fix N+1 problems, create indexes, configure PostgreSQL and EF Core, and implement caching or partitioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for implementation-level database design, PostgreSQL query optimization, indexing, EF Core migrations, caching, partitioning, monitoring, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a third-party API key and shows code that can send query plans to an external service. <br>
Mitigation: Only provide a scoped SkillBoss API key after trusting the provider and confirming privacy terms, token scope, and redaction expectations. <br>
Risk: Production schemas, SQL, logs, or query plans may contain sensitive operational or customer data. <br>
Mitigation: Redact sensitive database details before using external analysis and avoid sending production material unless the data handling process is approved. <br>
Risk: Generated SQL, index changes, or migration guidance can cause outages or data loss if applied directly. <br>
Mitigation: Treat output as advisory, test migrations outside production, maintain backups, and verify rollback plans before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/abe-database-operations) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with SQL, shell, C#, TypeScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory database examples and migration patterns; generated SQL should be reviewed and tested before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
