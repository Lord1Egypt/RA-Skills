## Description:

Generate database schemas, migrations, and ERD diagrams from plain English descriptions, with support for PostgreSQL, MySQL, SQLite, and MongoDB indexes and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matrixtrickery](https://clawhub.ai/user/matrixtrickery)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn plain English data model descriptions into database schemas, migration text, ERD diagrams, indexes, and seed data for application development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated schemas or migrations may contain incorrect assumptions or destructive changes if applied directly to a real database.

Mitigation: Review generated schema and migration output before use, and test changes in a staging database with backups or rollback plans before production.

Risk: Generated seed data may not match application, privacy, or compliance requirements.

Mitigation: Use seed data for development only unless it has been reviewed and adapted for the intended environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matrixtrickery/skills/db-schema-gen)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with SQL, JSON, and Mermaid or ASCII diagram content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can vary by database dialect, ORM target, diagram option, seed option, and requested format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
