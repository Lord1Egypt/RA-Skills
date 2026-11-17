## Description:

Query Digiforma training management platform via GraphQL API. Use when asked about trainees, sessions, invoices, programs, trainers, or any training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibbou](https://clawhub.ai/user/mibbou)

### License/Terms of Use:


## Use Case:

Developers and authorized Digiforma account users use this skill to query training management data such as trainees, training sessions, programs, invoices, and trainers through Digiforma's GraphQL API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve sensitive training, contact, and invoice data from a connected Digiforma account.

Mitigation: Install it only for authorized users and share trainee contact details or invoice information only when the requester has a legitimate need.

Risk: Broad GraphQL queries may return more Digiforma records or fields than needed.

Mitigation: Use pagination, narrow result fields, and apply search or status filters when possible.

Risk: Misuse or exposure of the Digiforma Bearer token can grant access to account data.

Mitigation: Store DIGIFORMA_API_KEY as a secret, avoid printing it in logs, and do not commit it to source files.

## Reference(s):

- [Digiforma GraphQL API endpoint](https://app.digiforma.com/api/v1/graphql)
- [ClawHub skill page](https://clawhub.ai/mibbou/skills/digiforma)
- [ClawHub publisher profile](https://clawhub.ai/user/mibbou)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands and GraphQL query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Bearer token authentication from the DIGIFORMA_API_KEY environment variable and recommends pagination for large result sets.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
