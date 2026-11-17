## Description:

Trigger when the user needs AI Web API aggregate search across web, news, shopping, or scholar sources, with optional extraction of result content; when multiple tools are enabled under one product, select tool_code according to the user intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can search web, shopping, news, and scholarly sources through Dataify's AI Web API, with optional extraction of page content. They can use the skill when an agent needs aggregated search results for a query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Dataify and may expose sensitive information.

Mitigation: Do not include confidential information in queries.

Risk: API requests can consume account credits.

Mitigation: Use the service with awareness of request costs and account limits.

Risk: The skill requires an API token to access the service.

Mitigation: Configure the token through the environment and retain the default HTTPS endpoint.

## Reference(s):

- [Search API reference](references/search-api.md)
- [Dataify AI Web API](https://aiwebapi.dataify.com)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-ai-web-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured search results with optional extracted page content in Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected search mode and query; page-content extraction is optional.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
