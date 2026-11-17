## Description:

Build type-safe database queries with Drizzle ORM patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers use this skill for Drizzle ORM query, schema, migration, driver, and performance guidance while building type-safe database-backed applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration guidance includes dev-only commands that can be destructive if applied to production databases.

Mitigation: Review database changes before applying them, use generated migrations for production, and reserve drizzle-kit push for development environments.

Risk: Documentation-only ORM guidance may not reflect the exact schema, driver, or migration state of a specific project.

Mitigation: Validate recommendations against the project configuration, Drizzle driver choice, and current migration history before changing application code or database state.

## Reference(s):

- [Drizzle ClawHub skill page](https://clawhub.ai/ivangdavila/skills/drizzle)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution, data access, or persistence behavior found in the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
