## Description:

Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emiltsoi](https://clawhub.ai/user/emiltsoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for planning database schema changes, data transformations, ORM migrations, rollback procedures, and zero-downtime deployment strategies across Sequelize, TypeORM, and Prisma.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact destructive migration and rollback examples may cause data loss if applied directly to production systems.

Mitigation: Use this skill as general reference, test plans in staging, require verified backups, and obtain explicit approval before destructive changes.

Risk: The checkpoint rollback example drops a live table during exception handling.

Mitigation: Avoid that pattern for live systems and use vetted recovery procedures or transaction-based rollback where appropriate.

Risk: Migration commands may run unexpected tooling versions if project dependencies are not pinned.

Mitigation: Pin migration tooling in project dependencies and run commands through lockfile-controlled local binaries.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with code blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration guidance and examples; it does not execute database commands directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
