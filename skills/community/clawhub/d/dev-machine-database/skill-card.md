## Description:

Connects to a development machine over SSH to query a MySQL dw database, inspect tables, count rows, and format query results for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a development MySQL data warehouse through SSH, including listing tables, checking schemas, running limited read queries, and summarizing row counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports hardcoded privileged database access and unsafe command construction that could expose or alter internal data.

Mitigation: Rotate exposed credentials, remove hardcoded passwords, use a dedicated read-only account, enforce an allowlist for SELECT, SHOW, and DESCRIBE-style operations, and avoid embedding SQL in SSH shell strings.

Risk: Database results may include sensitive internal information and the artifact describes sending formatted results to Feishu.

Mitigation: Require user confirmation before sharing query results externally and restrict the skill to environments where the operator controls the datax host and MySQL instance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexmayanjun-collab/skills/dev-machine-database)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and tabular query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented database lookup output; artifact behavior applies a default 50-row display limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
