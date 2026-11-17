## Description:

Design data models for construction projects. Create entity-relationship diagrams, define schemas, and generate database structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, data engineers, and construction project teams use this skill to design project data entities, relationships, schemas, ER diagrams, and draft database structures from user-provided project data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL may include unsuitable table names, column names, relationships, or constraints for the target database.

Mitigation: Review generated SQL manually, validate it against project requirements, and run it only in an appropriate database environment with limited privileges.

Risk: The skill requests filesystem access for project data workflows.

Mitigation: Install and use it only when file access is acceptable for the project data being processed.

## Reference(s):

- [Data Driven Construction](https://datadrivenconstruction.io)
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/data-model-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured tables, Mermaid ER diagrams, SQL DDL, JSON Schema, and validation findings as applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Excel, CSV, or JSON export formats when relevant.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
