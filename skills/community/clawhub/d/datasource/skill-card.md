## Description:

Guides an agent to build NocoBase data models with tables, fields, relations, and seed data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander-lq](https://clawhub.ai/user/alexander-lq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through NocoBase schema design, collection registration, field interface setup, relationship creation, and optional seed data insertion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to make broad NocoBase database changes.

Mitigation: Require review of planned SQL and API operations, confirm the target database, reject destructive or unrelated statements, and keep backups or rollback procedures available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexander-lq/skills/datasource)

## Skill Output:

**Output Type(s):** [Guidance, Code, API calls, Configuration]

**Output Format:** [Markdown with SQL and NocoBase tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SQL DDL, collection configuration, relation definitions, field interface settings, verification steps, and seed-data statements.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
