## Description:

Generates semantic YAML files from MySQL, SQL Server, PostgreSQL, Oracle, or Excel sources so agents can build semantic models and topic configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asksqlai](https://clawhub.ai/user/asksqlai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to discover database tables or Excel sheets, select relevant sources, and generate semantic YAML configuration files for downstream text-to-SQL workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database metadata, sampled values, enum values, and Excel sheet contents may be sent to AskSQL or a configured Excel API endpoint during YAML generation.

Mitigation: Use read-only, least-privileged, non-production credentials; avoid sensitive spreadsheets; choose narrow table or sheet selections; and approve API endpoints before running generation.

Risk: Generated semantic YAML may contain incorrect, overly broad, or sensitive metadata derived from sampled source data.

Mitigation: Review generated YAML in a safe output directory before giving it to another AI workflow or using it for text-to-SQL generation.

## Reference(s):

- [Open Semantic Interchange Field Specification](references/open_semantic_interchange_description.md)
- [AskSQL](https://www.asksql.ai)
- [ClawHub Skill Page](https://clawhub.ai/asksqlai/skills/database-semantic-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated YAML configuration files, and JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated YAML should be reviewed before use in another AI workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
