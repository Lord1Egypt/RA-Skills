## Description:

Generates Java/Spring Boot CRUD layers, Vue 2 admin pages, and SQL files from DDL table definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold CRUD implementation files from database DDL, including backend Java/Spring Boot classes, optional Vue 2 frontend files, SQL scripts, and validation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CRUD code may be under-scoped for tenant or ownership boundaries.

Mitigation: Review generated read, update, delete, list, count, and export operations before merging, add tenant or ownership checks, and derive operatorId from the authenticated user rather than client input.

Risk: Generated or templated SQL may include destructive DROP TABLE statements.

Mitigation: Treat destructive SQL as development-only unless deliberately approved, and review all generated SQL before applying it to shared or production databases.

Risk: Incorrect target paths could place generated files in the wrong project modules.

Mitigation: Use explicit target paths, confirm auto-detected backend and frontend structure, and review the generated file list before build or deployment.

## Reference(s):

- [Java Code Templates](references/java-templates.md)
- [SQL Templates](references/sql-templates.md)
- [Vue Frontend Templates](references/vue-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/endcy/skills/crud-code-generator)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and file-generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDL SQL and target project paths; may produce backend files, frontend files, SQL files, and validation commands.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact version table)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
