## Description: <br>
Generate Ecto migrations from natural language or schema descriptions, including tables, columns, indexes, constraints, references, enums, partitioning, reversible migrations, data migrations, and multi-tenant patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to draft and review Ecto database migrations for Elixir projects, including schema changes, indexes, constraints, references, enums, data migrations, and multi-tenant patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migrations can change or remove database data when users run operations such as dropping columns, changing data, cascading deletes, extensions, or raw SQL. <br>
Mitigation: Review every generated migration before running it, test database-impacting changes outside production first, and pay special attention to destructive or raw SQL operations. <br>
Risk: Data migrations and schema migrations may be unsafe when combined or run against large production tables without operational planning. <br>
Mitigation: Keep data migrations separate from schema migrations and use staged or batched approaches for large tables. <br>


## Reference(s): <br>
- [Column Types Reference](references/column-types.md) <br>
- [Index Patterns Reference](references/index-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Elixir and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; generated migrations should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
