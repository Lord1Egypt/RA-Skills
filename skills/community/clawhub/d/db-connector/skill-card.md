## Description:

Helps agents identify and avoid common database connection, transaction, schema change, backup and restore, replication, query performance, data integrity, and scalability pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database operators, and agent users use this skill to review database operation plans, match common failure modes, and choose safer practices for SQL queries, schema changes, backups, replication, and integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide schema changes, data updates, backup restores, command execution, API calls, and production database access.

Mitigation: Require explicit human review and confirmation before running any generated database operation, command, restore, or production-access step.

Risk: Database guidance may affect availability, data integrity, or sensitive data exposure if applied to the wrong environment or without validation.

Mitigation: Apply changes first in a test environment, verify backups and rollback paths, and confirm access controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/db-connector)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose database operations, commands, configuration changes, and validation steps for human review before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
