## Description:

Brave Search 极简国内版 uses the Brave API to run web searches through a local proxy with CN and zh-hans defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch current web, news, and video search results from Brave Search in environments that require a local HTTP proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Brave Search through the configured localhost proxy.

Mitigation: Use this skill only when Brave Search and the configured proxy are appropriate for the query data being sent.

Risk: The skill requires a Brave Search API key that may be stored in the agent environment.

Mitigation: Store the API key in the agent's supported environment configuration and rotate it if exposure is suspected.

Risk: Disabling built-in web search can route future searches through this skill's CN and zh-hans defaults.

Mitigation: Disable built-in web search only when that routing is intended, and adjust country or language parameters for other use cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhc888007/skills/brave-search-vpn)
- [Brave Search API endpoint](https://api.search.brave.com/res/v1/web/search)
- [Brave Search API keys](https://api-dashboard.search.brave.com/app/keys)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON string for search results; Markdown guidance for setup and usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_SEARCH_API_KEY and HTTP_PROXY_PORT; defaults include country=CN, search_lang=zh-hans, safesearch=moderate, count limited to 20, and offset limited to 9.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
