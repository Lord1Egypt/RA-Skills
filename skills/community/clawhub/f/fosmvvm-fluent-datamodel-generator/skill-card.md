## Description:

Generate Fluent DataModels for FOSMVVM server-side persistence. Scaffolds models, migrations, and tests for database-backed entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add database-backed entities to Swift Vapor/FOSMVVM applications that use Fluent. It guides creation of DataModel implementations, schema and seed migrations, tests, and migration registration while preserving FOSMVVM field separation and relationship patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migrations, seed data, cascade deletes, or raw SQL could alter database structure or data in ways that do not match the application's intent.

Mitigation: Review generated migrations, seed data, cascade delete behavior, and raw SQL before running them against a real database.

Risk: Using the skill in a project that does not use Fluent could produce inappropriate persistence-layer code.

Mitigation: Install and invoke it only for Swift Vapor/FOSMVVM projects that actually use Fluent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foscomputerservices/skills/fosmvvm-fluent-datamodel-generator)
- [FOSUtilities homepage](https://github.com/foscomputerservices/FOSUtilities)
- [Reference templates](reference.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Swift code templates and migration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed project files and edits for Fluent DataModels, migrations, tests, and database registration.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
