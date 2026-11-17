## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aysun168](https://clawhub.ai/user/aysun168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send web-search queries to Baidu AI Search Engine for live information, documentation lookup, and research, with optional result count and freshness filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search query text is sent to Baidu's external API.

Mitigation: Avoid sensitive, private, or proprietary search terms and review data-handling requirements before use.

Risk: BAIDU_API_KEY is a secret used by the search script.

Mitigation: Store the key only in approved environment or OpenClaw configuration paths, restrict local config access, and do not commit or share the key.

## Reference(s):

- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [ClawHub Skill Page](https://clawhub.ai/aysun168/skills/baidu-search-bak)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; accepts query, count, and freshness parameters; returns Baidu reference results with snippets removed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
