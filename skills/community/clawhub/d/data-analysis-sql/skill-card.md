## Description:

Data Analysis SQL helps agents draft, revise, optimize, and migrate SQL across common data engines while supporting data warehouse modeling, ETL planning, data quality checks, and Markdown knowledge-base generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whiskeyforsun](https://clawhub.ai/user/whiskeyforsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analytics engineers use this skill to produce SQL, review and migrate SQL dialects, design warehouse layers, plan ETL flows, check data quality, and generate Markdown documentation for schemas, metrics, relations, and enums.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL for multi-tenant data can mix tenant data if JOINs or filters omit tenant constraints.

Mitigation: Review generated SQL before use, especially every JOIN, and require tenant filters wherever tenant-bearing tables are involved.

Risk: Broad document-generation triggers can summarize or write private spreadsheets, schemas, or metric SQL too readily.

Mitigation: Use document-generation behavior only when the user explicitly asks to summarize or write those materials to a chosen path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whiskeyforsun/skills/data-analysis-sql)
- [SQL Guide](references/sql-guide.md)
- [Join Rules](references/join-rules.md)
- [SQL Pitfalls](references/sql-pitfalls.md)
- [Business Metrics](references/business-metrics.md)
- [Schema Guide](references/schema-guide.md)
- [Multi-Engine Dialect Reference](references/multi-engine.md)
- [Pipeline Patterns](references/pipeline-patterns.md)
- [Data Quality](references/data-quality.md)
- [Data Analysis Patterns](references/data-analysis-patterns.md)
- [Knowledge Base](references/knowledge-base.md)
- [Documentation Guide](references/doc-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, SQL, Python snippets, shell commands, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Markdown documentation files when the user explicitly requests a chosen output path.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
