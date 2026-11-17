## Description:

APIClaw Amazon API helps agents answer APIClaw capability and integration questions for six Amazon commerce-data endpoints covering categories, markets, products, competitors, realtime product detail, and review analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christine-srp](https://clawhub.ai/user/christine-srp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to understand APIClaw's Amazon commerce-data endpoints, required API key setup, request shapes, response fields, credit use, and endpoint-specific quirks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API queries and APICLAW_API_KEY are sent to APIClaw.

Mitigation: Store the key in the environment, avoid pasting it into logs or shared transcripts, and tell users when APIClaw will receive query data.

Risk: API calls consume credits and are subject to rate limits.

Mitigation: Check credit usage before large runs, monitor creditsConsumed and creditsRemaining, and throttle requests to stay within documented limits.

Risk: Endpoint response fields differ, and some commerce metrics are estimates or delayed.

Mitigation: Use the endpoint-specific field reference, surface uncertainty for lower-bound or delayed data, and avoid assuming fields are shared across endpoints.

## Reference(s):

- [APIClaw API Quick Reference](references/openapi-reference.md)
- [APIClaw API Docs](https://api.apiclaw.io/api-docs)
- [APIClaw Live OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec)
- [APIClaw Website](https://apiclaw.io)
- [APIClaw Pricing](https://apiclaw.io/pricing)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint-specific request examples, response field guidance, API-key setup instructions, credit-use notes, and caveats about endpoint differences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
