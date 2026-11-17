## Description:

Run safe read-only queries against MySQL or PostgreSQL for data inspection, reporting, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect PostgreSQL or MySQL schemas, run read-only reporting queries, count rows, sample data, troubleshoot database state, and optionally export query results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The read-only claim is not a hard security boundary.

Mitigation: Use a dedicated read-only database user or read replica, and do not run the skill with owner or administrator credentials.

Risk: The export option can overwrite arbitrary local files.

Mitigation: Avoid using --out unless exports are constrained to a safe directory and overwrite behavior is reviewed.

Risk: Queries can expose sensitive database contents.

Mitigation: Limit queries to approved datasets, prefer scoped SELECT statements with LIMIT for exploration, and avoid printing secrets from environment variables.

## Reference(s):

- [Query Cookbook (Read-Only)](references/query-cookbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce database query output in table, CSV, TSV, or JSON form when the bundled shell script is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
