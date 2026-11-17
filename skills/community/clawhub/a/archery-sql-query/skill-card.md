## Description:

Archery SQL Query helps agents query databases through an Archery SQL platform, inspect schemas, list instances, databases, and tables, run reusable query templates, and find duplicate records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ming1007520388](https://clawhub.ai/user/ming1007520388)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to run SQL queries through Archery, inspect database and table structure, manage instance aliases, and generate duplicate-record reports or deletion SQL for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles database credentials and reusable sessions.

Mitigation: Use HTTPS, least-privilege or read-only Archery accounts where possible, and protect ~/.archery files with restrictive permissions.

Risk: The skill can execute arbitrary SQL against configured Archery instances.

Mitigation: Review SQL before execution and prefer bounded read queries with explicit LIMIT clauses.

Risk: Duplicate detection can generate DELETE statements.

Mitigation: Manually review generated DELETE SQL and run it only after database-owner approval and backup checks.

## Reference(s):

- [Archery Query Configuration Example](references/config-example.md)
- [Supported Database Types](references/database-types.md)
- [Table Structure Query Guide](references/table-structure-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, shell commands, configuration snippets, and optional table or JSON query output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated SQL files and CSV duplicate-record reports when duplicate detection scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
