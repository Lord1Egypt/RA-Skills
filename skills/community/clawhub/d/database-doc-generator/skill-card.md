## Description:

Generate professional database structure documentation from PostgreSQL databases, including Excel files with table schemas, column details, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitoftom](https://clawhub.ai/user/gitoftom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect PostgreSQL schema metadata and generate data dictionaries or database structure documentation for selected tables or entire public schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the package ships real-looking historical credential material and broad cleanup tooling that can rewrite or delete project files.

Mitigation: Do not install it as-is in sensitive environments; ask the maintainer to redact historical credential material and isolate or remove credential-cleanup tooling before production use.

Risk: Database credentials may be exposed through command-line arguments, JSON configuration, logs, or checked-in files.

Mitigation: Use protected environment variables or a secrets manager, avoid passwords on the command line, and test only with a read-only database account.

Risk: Generated Excel files can reveal table names, column names, comments, and other sensitive schema metadata.

Mitigation: Write outputs to a private directory, restrict file permissions, and review or redact sensitive fields before sharing.

Risk: Database connections may be unencrypted or broader than necessary.

Mitigation: Require TLS settings, limit network access, and grant only the metadata permissions needed for schema documentation.

## Reference(s):

- [SQL Queries](references/SQL_QUERIES.md)
- [Excel Formatting Guide](references/EXCEL_FORMATTING.md)
- [Usage Examples](references/USAGE_EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; generated output is a formatted Excel workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PostgreSQL network access and Python dependencies; output workbooks may contain sensitive schema metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
