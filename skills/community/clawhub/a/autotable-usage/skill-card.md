## Description:

Provides Chinese guidance for using AutoTable, a JDBC-based Java framework for automatically maintaining database schemas across nine supported databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imtzc](https://clawhub.ai/user/imtzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for AutoTable installation, annotation, configuration, extension, lifecycle, SQL audit, data initialization, multi-data-source, and database-specific guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated AutoTable configuration or examples can modify, recreate, or drop database schema objects when applied to real databases.

Mitigation: Keep production in validate or none mode unless changes are reviewed, disable auto-drop-table and auto-drop-column outside disposable environments, and back up data before applying schema changes.

Risk: Database administrator credentials may be needed for automatic database creation examples.

Mitigation: Provide database credentials through a secret manager or environment variables rather than committing them in configuration files.

## Reference(s):

- [Server-resolved source repository](https://github.com/dromara/auto-table-claude-plugin)
- [AutoTable quick start](references/quick-start.md)
- [AutoTable annotation reference](references/annotation-reference.md)
- [AutoTable configuration reference](references/configuration.md)
- [AutoTable lifecycle callbacks and interceptors](references/lifecycle.md)
- [AutoTable database-specific guidance](references/database-specific.md)
- [AutoTable type mapping](references/type-mapping.md)
- [AutoTable multi-data-source guidance](references/multi-datasource.md)
- [AutoTable best practices](references/best-practices.md)
- [AutoTable architecture and extension guide](references/architecture.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Java, XML, Gradle, YAML, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no tool or API calls are invoked by the skill.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
