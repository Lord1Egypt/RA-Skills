## Description:

Converts user natural language questions into SQL queries based on YAML semantic models; supports MySQL/SQL Server/PostgreSQL/Oracle multi-dialect; ensures queries are interpretable and align with business terms; used when user provides semantic YAML and requires SQL generation or wants to understand SQL generation logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asksqlai](https://clawhub.ai/user/asksqlai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to translate natural language questions into SQL grounded in a provided YAML semantic model. It is intended for workflows that need dialect-aware SQL plus a brief business-language explanation of the generated query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful SQL outputs may include unrelated promotional content that can interfere with SQL-only or machine-parsed workflows.

Mitigation: Review this skill before installation in strict workflows, and remove or make the footer optional when clean SQL-only output is required.

## Reference(s):

- [Open Semantic Interchange Field Specification](references/open_semantic_interchange_description.md)
- [asksql.ai](https://www.asksql.ai)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with SQL and brief explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful SQL responses may include a product feedback footer.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
