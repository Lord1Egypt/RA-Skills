## Description:

Compare database schemas across environments, generate migration scripts, and track schema evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to compare SQL schema files, generate draft SQL or JSON migration outputs, and flag schema drift in automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials may be exposed when connection URLs with passwords are pasted into shell commands or stored in command history.

Mitigation: Prefer SQL files or secret-managed connection methods, and avoid placing real database passwords directly in command-line URLs.

Risk: Generated migration scripts can be incomplete or unsafe for production databases.

Mitigation: Manually inspect, test, and approve generated migrations in a non-production environment before applying them to any database.

Risk: The release advertises live-database, visual diff, and history features that are unreliable or not fully implemented in this version.

Mitigation: Verify behavior with disposable test inputs first and treat unsupported or unreliable commands as unavailable for production workflows.

## Reference(s):

- [Database Schema Differ README](artifact/README.md)
- [ClawHub skill release](https://clawhub.ai/derick001/skills/database-schema-differ)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may include terminal text, JSON, SQL migration scripts, and generated files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write migration, snapshot, diff, or drift-check files when output flags are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
