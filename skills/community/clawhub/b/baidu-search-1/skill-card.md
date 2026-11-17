## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzmtxh](https://clawhub.ai/user/bzmtxh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live Baidu web searches for current information, documentation lookup, and research topics. It accepts a search query with optional result count and freshness filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu through a third-party API.

Mitigation: Install only when this data sharing is acceptable for the intended use case.

Risk: The skill depends on a Baidu API key stored in the local agent environment or OpenClaw configuration.

Mitigation: Protect the configuration with owner-only permissions, avoid sharing the full config, use a dedicated low-privilege key where possible, and rotate the key if exposure is suspected.

## Reference(s):

- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu Qianfan AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON search results printed to stdout, with status and error text when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; supports query, count, and freshness inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
