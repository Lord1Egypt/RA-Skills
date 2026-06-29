## Description: <br>
Provides database performance optimization guidance for SQL query tuning, index strategy, execution-plan analysis, ORM tuning, connection pools, locks, and monitoring across PostgreSQL, MySQL, and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this Chinese-language skill to diagnose slow queries, design indexes, interpret query plans, tune ORM access patterns, adjust connection pools, and investigate locking or monitoring issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested SQL or database setting changes may affect availability, performance, or data integrity if applied directly. <br>
Mitigation: Review each recommendation against the actual schema, test in a controlled environment, keep backups, and require approval before running changes such as CREATE INDEX, SET GLOBAL, or CREATE EXTENSION. <br>
Risk: Optimization advice can be misleading without current measurements from the target database. <br>
Mitigation: Collect baselines, query plans, and monitoring data before changing indexes, SQL, ORM loading behavior, or connection-pool settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/database-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
