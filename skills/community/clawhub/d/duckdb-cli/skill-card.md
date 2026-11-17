## Description:

DuckDB CLI specialist for SQL analysis, data processing and file conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proxx](https://clawhub.ai/user/proxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to ask an agent for DuckDB CLI guidance, SQL examples, file inspection commands, and CSV, Parquet, or JSON conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested DuckDB commands may read local datasets or expose data through query output.

Mitigation: Review file paths, selected columns, filters, and output destinations before running generated commands.

Risk: Conversion and export examples can write files or modify DuckDB databases.

Mitigation: Use read-only mode for inspection when possible and confirm target filenames before executing COPY, INSERT, CREATE TABLE, or export commands.

Risk: Configuration or editor guidance may affect the local DuckDB CLI environment.

Mitigation: Review changes to ~/.duckdbrc and external editor use before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/proxx/skills/duckdb-cli)
- [DuckDB CLI Overview](https://duckdb.org/docs/stable/clients/cli/overview)
- [DuckDB CLI Arguments](https://duckdb.org/docs/stable/clients/cli/arguments)
- [DuckDB Dot Commands](https://duckdb.org/docs/stable/clients/cli/dot_commands)
- [DuckDB Output Formats](https://duckdb.org/docs/stable/clients/cli/output_formats)
- [DuckDB CLI Editing](https://duckdb.org/docs/stable/clients/cli/editing)
- [DuckDB CLI Autocomplete](https://duckdb.org/docs/stable/clients/cli/autocomplete)
- [DuckDB Syntax Highlighting](https://duckdb.org/docs/stable/clients/cli/syntax_highlighting)
- [DuckDB Safe Mode](https://duckdb.org/docs/stable/clients/cli/safe_mode)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read local datasets, write output files, modify DuckDB databases, or change DuckDB CLI configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
