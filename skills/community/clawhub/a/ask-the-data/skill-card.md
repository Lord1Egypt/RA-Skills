## Description:

Part of the Overpowered skill suite, ask-the-data helps agents answer reproducible questions from local structured data files by discovering useful inputs, consulting dictionaries, querying only what is needed, and returning traceable results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data-focused agents use this skill to answer questions from local tabular and structured data such as Excel, CSV, JSON, TSV, and Parquet files. It is best suited for tasks that need dictionary-aware schema inspection, focused querying, validation checks, and evidence that makes the answer reproducible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local structured datasets and may use optional DuckDB persistence or generated outputs.

Mitigation: Install it only in projects where agent access to the local data is acceptable, and confirm where any DuckDB database or generated outputs will be stored.

Risk: Answers can be misleading if column names, codes, units, dates, currencies, or identifiers are interpreted without supporting definitions.

Mitigation: Use available data dictionaries or codebooks, inspect schemas and representative samples, and validate suspicious results with counts, uniqueness checks, null checks, or targeted samples.

## Reference(s):

- [Project Conventions](references/project-conventions.md)
- [Overpowered suite](https://github.com/raguets/overpowered)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown answer with evidence bullets and optional SQL or query summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source files or tables, business definitions used, filters and assumptions, query provenance, and validation checks when relevant.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
