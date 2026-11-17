## Description:

Generate API integrations from OpenAPI/Swagger specs, including MCP servers, API clients, and webhook handlers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn OpenAPI or Swagger specifications, or API documentation, into scaffolded REST API integrations. It is intended for generating MCP server code, Python clients, webhook handlers, authentication patterns, retries, rate limiting, and verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated integrations may send credentials to unintended API hosts or OAuth token endpoints.

Mitigation: Use trusted OpenAPI specs, verify every base URL and token endpoint, and keep secrets out of prompts and logs.

Risk: Generated file-upload or write/delete API actions may expose local files or modify remote data.

Mitigation: Require explicit approval before executing upload, write, or delete operations, and verify both the selected file and destination service.

Risk: Runnable scaffolds may be incomplete or unsafe for a specific API's authentication, pagination, rate-limit, or error semantics.

Mitigation: Review and test generated code against the API documentation before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/skills/gavin-api-bridge)
- [GitHub OpenAPI Spec](https://api.github.com/openapi.json)
- [Stripe OpenAPI Spec](https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json)
- [Twilio OpenAPI Spec](https://github.com/twilio/twilio-oai/blob/main/spec/yaml/twilio_api_v2010.yaml)
- [OpenAI OpenAPI Spec](https://github.com/openai/openai-openapi/blob/main/openapi.yaml)
- [Notion OpenAPI Spec](https://github.com/makenotion/notion-sdk-js/blob/main/api-openapi.yml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce runnable integration scaffolds that require review, credential configuration, and endpoint validation before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
