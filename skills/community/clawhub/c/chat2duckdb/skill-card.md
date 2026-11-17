## Description:

Chat2DuckDB helps agents inspect local tabular datasets, run DuckDB SQL queries, sample data, correct common SQL errors, and export analysis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcba](https://clawhub.ai/user/cloudcba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and agents use this skill to explore CSV, JSON, Parquet, and Excel files, generate or refine DuckDB SQL, execute queries, and save result files. It is suited for local data profiling, ad hoc analysis, sampling, and report-oriented query workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local DuckDB SQL, file-read, file-write, and persistence behavior can expose or retain sensitive data.

Mitigation: Use the skill only with trusted datasets and approved writable paths; treat exported files and persistent DuckDB databases as sensitive retained data.

Risk: Untrusted SQL or hostile file headers can lead to unsafe or misleading query behavior.

Mitigation: Avoid untrusted SQL and hostile datasets; preview or query results before saving outputs.

## Reference(s):

- [Data formats guide](references/data-formats.md)
- [ClawHub skill page](https://clawhub.ai/cloudcba/skills/chat2duckdb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline SQL, shell commands, and file output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local CSV, Excel, JSON, Parquet, and DuckDB database files when users request exported or persisted results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
