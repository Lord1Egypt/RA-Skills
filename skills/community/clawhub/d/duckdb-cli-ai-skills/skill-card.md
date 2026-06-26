## Description: <br>
DuckDB CLI specialist for SQL analysis, data processing, and file conversion with CSV, Parquet, JSON, and DuckDB databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CamelSprout](https://clawhub.ai/user/CamelSprout) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data analysts, and engineers use this skill to ask an agent for DuckDB CLI commands, SQL examples, data conversion steps, output formatting guidance, and safer inspection patterns for local data files and DuckDB databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DuckDB commands may read local files or write exports to unintended destinations through paths, globs, COPY targets, or output directives. <br>
Mitigation: Review generated commands before running them, especially input paths, globs, COPY/export destinations, .output targets, and editor commands. <br>
Risk: Inspection tasks against existing DuckDB databases can become write-capable if commands omit read-only mode. <br>
Mitigation: Prefer read-only mode for existing databases when the task only requires inspection. <br>


## Reference(s): <br>
- [DuckDB CLI Overview](https://duckdb.org/docs/stable/clients/cli/overview) <br>
- [DuckDB CLI Arguments](https://duckdb.org/docs/stable/clients/cli/arguments) <br>
- [DuckDB CLI Dot Commands](https://duckdb.org/docs/stable/clients/cli/dot_commands) <br>
- [DuckDB CLI Output Formats](https://duckdb.org/docs/stable/clients/cli/output_formats) <br>
- [DuckDB CLI Editing](https://duckdb.org/docs/stable/clients/cli/editing) <br>
- [DuckDB CLI Autocomplete](https://duckdb.org/docs/stable/clients/cli/autocomplete) <br>
- [DuckDB CLI Syntax Highlighting](https://duckdb.org/docs/stable/clients/cli/syntax_highlighting) <br>
- [DuckDB CLI Safe Mode](https://duckdb.org/docs/stable/clients/cli/safe_mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
