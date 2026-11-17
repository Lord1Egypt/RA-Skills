## Description:

Provides API guidance for retrieving Feishu crypto group summaries, contract-address lookups, popular token statistics, KOL analysis, market news, and on-chain token data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hengxuz](https://clawhub.ai/user/hengxuz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query a third-party crypto community API for token discussion context, group-chat summaries, KOL commentary, market news, and API token usage status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and group-chat queries are documented over an unencrypted HTTP endpoint.

Mitigation: Require HTTPS or another trusted transport before sending real tokens, and use narrowly scoped, revocable credentials.

Risk: Group-chat summaries may include authorization-limited community content.

Mitigation: Only query, store, or redistribute summaries when the user has permission, and redact sensitive content before sharing.

Risk: KOL, token, and market outputs may be incomplete, stale, promotional, or otherwise unsuitable as financial advice.

Mitigation: Treat results as informational and verify with independent market and on-chain sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hengxuz/skills/cryptojuhequn)
- [API documentation](http://88.222.241.169/static/skill.md)
- [Swagger UI](http://88.222.241.169/docs)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bearer token; the documented service returns JSON and is rate-limited to 500 calls per token per day.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
