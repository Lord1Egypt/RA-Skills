## Description: <br>
Run safe read-only queries against MySQL or PostgreSQL for data inspection, reporting, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data practitioners use this skill to inspect schemas, sample data, count rows, troubleshoot database state, and export read-only query results from PostgreSQL or MySQL without modifying data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using write-capable or administrative database credentials can increase impact if a query or environment is misconfigured. <br>
Mitigation: Use a dedicated read-only database account and review each query before execution. <br>
Risk: The --out option can overwrite files writable by the current user. <br>
Mitigation: Export only to intentional, safe paths and verify the destination before running the command. <br>
Risk: Large unrestricted reads can expose more data than needed or strain database resources. <br>
Mitigation: Prefer LIMIT clauses and scoped filters for exploratory queries. <br>


## Reference(s): <br>
- [DB Readonly ClawHub release](https://clawhub.ai/reed1898/db-readonly) <br>
- [Query Cookbook](references/query-cookbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and database query outputs in table, CSV, TSV, or JSON formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can export query output to a user-selected file path when --out is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
