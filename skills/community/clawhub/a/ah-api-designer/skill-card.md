## Description:

API Designer helps agents design REST, GraphQL, OpenAPI/Swagger, versioning, authentication, and authorization patterns for API-first development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft API specifications, endpoint and schema designs, authentication patterns, client SDK examples, testing strategies, and migration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated client code may mishandle authentication, retry limits, token refresh, or where API keys and bearer tokens are sent.

Mitigation: Review generated client code before production use, with specific attention to authentication handling, retry behavior, token refresh, and credential destinations.

Risk: Generated API specifications or SDK patterns may be incomplete or unsuitable for the target service.

Mitigation: Validate generated specifications, schemas, tests, and migration guidance against the service requirements before deployment.

## Reference(s):

- [Api Designer Code Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with API specifications, schema examples, client SDK code, testing strategies, security considerations, and migration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated client code and API security details before production use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
