## Description:

Database-agent helps Java backend developers analyze slow SQL, inspect schema compliance, validate risky data correction statements, and generate database test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningwang770](https://clawhub.ai/user/ningwang770)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to review SQL performance, check table design standards, assess data update or delete safety, and produce structured test data for backend database workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes raw SQL execution paths that may read or change a database without enforcing all documented safety checks.

Mitigation: Use least-privilege database accounts, prefer read-only access for analysis, and require separate human review before any generated or executed data change.

Risk: Generated SQL, backup or rollback scripts, and reports may be incomplete or unsafe for a production database.

Mitigation: Test changes outside production, confirm backups and rollback plans, use transaction controls, and treat generated reports and SQL as untrusted until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningwang770/skills/database-agent)
- [SQL optimization rules](references/sql_optimization_rules.md)
- [Database design standards and naming conventions](references/database_standards.md)
- [Safe database operation guidelines](references/safe_operation_guidelines.md)
- [Test data generation patterns](references/test_data_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with JSON reports, SQL snippets, shell commands, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SQL recommendations, backup or rollback script templates, Excel-oriented report data, and generated test-data statements for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
