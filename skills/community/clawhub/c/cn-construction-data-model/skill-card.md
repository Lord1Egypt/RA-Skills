## Description:

Designs construction project data models, including entity-relationship diagrams, schemas, and database structures aligned with GB/T construction standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Construction data teams, developers, and project analysts use this skill to model project lifecycle data, define entities and relationships, and draft SQL, JSON schema, and Mermaid ER diagram outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL schemas or database structures may be incorrect, incomplete, or unsafe to apply directly.

Mitigation: Review generated DDL and schemas before use, test them in a non-production database, and adapt dialect-specific details before deployment.

Risk: Untrusted project data could introduce problematic identifiers, comments, or default values into generated schema output.

Mitigation: Validate user-provided fields and project data before generation, especially names, comments, defaults, and relationship definitions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ruiyongwang/skills/cn-construction-data-model)
- [Mermaid Live Editor](https://mermaid.live)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, SQL, JSON, Guidance]

**Output Format:** [Markdown with tables and code blocks for SQL DDL, JSON Schema, and Mermaid ER diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts based on user-provided construction project data and should be reviewed before applying database changes.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
