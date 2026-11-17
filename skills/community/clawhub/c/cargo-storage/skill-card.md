## Description:

Inspect and manage business data in a Cargo workspace, including models, datasets, columns, relationships, records, and SQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage structured business data in Cargo workspaces, including schema changes, records, relationships, and SQL queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook setup may expose a workspace access key with more permissions than needed, especially when selecting the first listed token or putting a token in a URL.

Mitigation: Choose a token explicitly and check its permissions, transfer credentials privately, and use an authorization header where supported. Revoke any privileged token already exposed through a shared URL.

## Reference(s):

- [Model examples](references/examples/models.md)
- [Dataset examples](references/examples/datasets.md)
- [Column examples](references/examples/columns.md)
- [Storage query examples](references/examples/queries.md)
- [Webhook ingest examples](references/examples/ingest-webhook.md)
- [Response shapes](references/response-shapes.md)
- [Troubleshooting](references/troubleshooting.md)
- [Project homepage (skill metadata)](https://github.com/getcargohq/cargo-skills)

## Skill Output:

**Output Type(s):** [Shell commands, SQL queries, Configuration guidance, Webhook request examples]

**Output Format:** [Markdown with inline shell and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and queries are tailored to the active Cargo workspace; write commands can change workspace data.]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
