## Description:

Real-time Chinese web search powered by 360's search engine API for current web, news, company, product, regulatory, and market-data queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rybobo](https://clawhub.ai/user/rybobo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route current-information requests to 360's Chinese web search API and return source-backed results. It is especially suited for Chinese-language search, recent news, and China-specific companies, products, policies, and market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and a per-request session identifier are sent to 360's API.

Mitigation: Install only when 360 may receive the user's search queries, and avoid sending sensitive queries unless that data sharing is acceptable.

Risk: The skill depends on a billable SEARCH_360_API_KEY credential.

Mitigation: Store the API key in a dedicated secret manager or session-specific environment, and monitor provider usage or billing controls.

Risk: Credential setup guidance may include provider promotional text when the key is missing or invalid.

Mitigation: Review the user-facing setup response before deploying in environments where promotional messaging is restricted.

## Reference(s):

- [360 AI Platform](https://ai.360.com/platform)
- [ClawHub skill page](https://clawhub.ai/rybobo/skills/360-web-search)
- [Publisher profile](https://clawhub.ai/user/rybobo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search results with source URLs, freshness metadata, and setup guidance when credentials are missing or invalid]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEARCH_360_API_KEY and outbound HTTPS access to api.360.cn; results may include provider AI summaries and promotional setup text.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact frontmatter and config report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
