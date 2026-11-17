## Description:

Generate Ecto migrations from natural language or schema descriptions, including tables, columns, indexes, constraints, references, enums, partitioning, reversible migrations, data migrations, and multi-tenant patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to draft and review Ecto database migrations for Elixir applications, including schema changes, indexing, constraints, foreign keys, enum handling, data migrations, and multi-tenant patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migrations may include destructive operations such as dropping columns, dropping tables, renames, or cascading deletes.

Mitigation: Treat generated migrations as draft code; review destructive operations and confirm backups and rollback plans before applying them to production.

Risk: Schema changes and index creation can lock or slow production databases when applied without an appropriate migration strategy.

Mitigation: Review large-table changes, use separate migrations for concurrent indexes when appropriate, and validate rollback behavior before deployment.

Risk: Data migrations can be irreversible or unsafe when mixed with schema changes.

Mitigation: Keep schema changes and data changes in separate migrations and define explicit up/down behavior for irreversible operations.

## Reference(s):

- [Column Types Reference](references/column-types.md)
- [Index Patterns Reference](references/index-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Elixir, SQL, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft migration guidance and examples for human review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
