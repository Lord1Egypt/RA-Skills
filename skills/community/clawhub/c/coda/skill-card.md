## Description:

General-purpose Coda document manager via REST API v1 for listing, creating, updating, and deleting docs, tables, rows, pages, automations, and document structure using a Coda API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x7466](https://clawhub.ai/user/0x7466)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and manage Coda documents through the Coda REST API, including document discovery, table and row operations, page listing, automation triggers, and data export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete Coda documents and rows available to the API token.

Mitigation: Review mutating commands before execution, keep confirmation prompts enabled, and use --force only for deliberate automation.

Risk: The Coda API token can expose documents and row data available to the user.

Mitigation: Prefer CODA_API_TOKEN over command-line tokens, use the least access needed for the task, and handle JSON or CSV exports as sensitive data.

Risk: Retries or repeated execution may repeat mutating operations.

Mitigation: Check command results and request IDs before retrying create, insert, update, delete, or automation-trigger commands.

## Reference(s):

- [ClawHub Coda skill page](https://clawhub.ai/0x7466/skills/coda)
- [Coda API documentation](https://coda.io/developers/apis/v1)
- [Coda OpenAPI specification](https://coda.io/apis/v1/openapi.yaml)
- [Coda API rate limits](https://coda.io/developers/apis/v1#section/Rate-Limiting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, CSV]

**Output Format:** [Markdown guidance with shell command examples; CLI responses may be tables, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CODA_API_TOKEN; mutating requests act on Coda documents available to the token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
