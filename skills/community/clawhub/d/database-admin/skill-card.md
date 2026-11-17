## Description:

Provides PostgreSQL database administration support for schema design, bulk data operations, complex queries, query optimization, backup and restore, migrations, type handling, transactions, and database error troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericyang1234](https://clawhub.ai/user/ericyang1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to generate database administration guidance, SQL, shell commands, and supporting scripts for PostgreSQL schema changes, bulk loading, query analysis, backups, restores, migrations, JSONB and BIGINT handling, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a real-looking PostgreSQL administrator credential in the skill.

Mitigation: Do not install as published unless you own the referenced database and have rotated the exposed password; replace hardcoded secrets with environment variables or a secret manager.

Risk: The release evidence reports high-impact database and file operations without adequate safeguards.

Mitigation: Use least-privilege database roles and require confirmation, dry-run review, and backups before destructive or state-changing actions.

Risk: The release evidence recommends validating or safely quoting SQL identifiers before real database use.

Mitigation: Validate table, column, and index identifiers and use safe SQL construction patterns before executing generated statements.

## Reference(s):

- [Database Schema Guidelines](references/DB_SCHEMA.md)
- [Usage Guide](references/USAGE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable database commands or scripts that require review before use.]

## Skill Version(s):

2.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
