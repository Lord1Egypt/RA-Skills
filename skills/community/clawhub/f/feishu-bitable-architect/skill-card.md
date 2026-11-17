## Description:

A Chinese-language skill that helps users diagnose business needs and design implementation-ready Feishu Bitable table structures, fields, relationships, views, and automation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to turn vague Feishu Bitable or management-system requests into clear schema proposals before another tool creates the tables. It is useful for CRM, content operations, project/task tracking, orders, recruiting, knowledge management, and custom workflow design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated table, field, view, or automation proposals may not match the user's real business workflow or may affect business records if executed without review.

Mitigation: Review the proposed structures and automations before approving any downstream Feishu Bitable changes.

## Reference(s):

- [README](README.md)
- [Business Templates](references/business-templates.md)
- [Common Patterns](references/common-patterns.md)
- [Field Types Guide](references/field-types-guide.md)
- [Validation Rules](references/validation-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown proposal with diagnostic questions, table schemas, field definitions, relationships, views, automation suggestions, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance only; actual Feishu Bitable changes are intended to be performed by a downstream tool after review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
