## Description:

Python-based database connectivity skill supporting MySQL, PostgreSQL, Oracle, SQL Server, and SQLite with connection management, parameterized query execution, schema introspection, and transaction management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jami-lin](https://clawhub.ai/user/jami-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through connecting to relational databases, running SQL queries, applying updates, managing transactions, and inspecting schema metadata. It is useful when an agent needs database access workflows rather than text-only analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database accounts used through the skill can read or mutate data, including production data.

Mitigation: Use least-privilege database accounts and avoid production mutation unless it is explicitly intended and reviewed.

Risk: Untrusted SQL files executed with batch mode can run database-changing statements without parameter binding.

Mitigation: Use --batch only with trusted SQL and prefer parameterized query or update execution for user-provided values.

Risk: Credentials or secrets can be exposed through command-line arguments, database URLs, shell expansion, or shared-machine connection metadata.

Mitigation: Use environment variables, avoid literal passwords and embedded URL credentials, and move the connection store to a private protected location on shared machines.

Risk: Connections may lack enforced transport protection.

Mitigation: Require TLS for database connections before using the skill with sensitive or network-accessible databases.

## Reference(s):

- [Connection management](references/connection-pooling.md)
- [Query execution](references/query-execution.md)
- [Supported databases](references/supported-databases.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce database query results, schema summaries, connection guidance, and command-line usage examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
