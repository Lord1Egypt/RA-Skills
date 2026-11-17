## Description:

Database Optimization helps agents analyze database performance issues, optimize SQL, design indexes, inspect query plans, tune ORM usage, and adjust connection pools for PostgreSQL, MySQL, and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose slow queries, improve index strategy, review query plans, tune ORM behavior, adjust connection pools, investigate locks, and monitor PostgreSQL, MySQL, and SQLite database performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL, schema changes, or database settings may be unsuitable for a production workload.

Mitigation: Review execution plans, test changes in staging, back up important data, and obtain DBA approval before applying production schema changes or global database settings.

Risk: Performance recommendations may be misleading without workload measurements.

Mitigation: Establish baseline metrics, apply changes incrementally, and verify performance after each change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/database-optimization)
- [Skill Source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory database tuning recommendations; review and test before applying.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
