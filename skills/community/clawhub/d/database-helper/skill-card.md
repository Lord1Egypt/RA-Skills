## Description:

Database Helper assists with SQL construction, schema management, database queries, table creation, and related database operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users can use this skill for database-related assistance, including drafting SQL, reasoning about schema changes, and planning common database management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest destructive SQL or schema-changing operations such as CREATE, DROP, or other data-changing commands.

Mitigation: Manually review generated SQL, confirm the target environment, verify backups, and prepare a rollback plan before execution.

Risk: Broad activation around database and SQL requests can produce rough or context-incomplete guidance.

Mitigation: Treat outputs as draft guidance and validate them against the actual database schema, permissions, and operational requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/database-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, code, command, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before applying destructive SQL or schema changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
