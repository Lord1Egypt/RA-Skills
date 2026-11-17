## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyafeichina](https://clawhub.ai/user/liyafeichina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Baidu web search results for Chinese-language live information, documentation lookup, news, and research topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu and may appear in local logs or shared screenshots.

Mitigation: Use only queries appropriate for Baidu processing, avoid sharing logs or screenshots containing sensitive query text, and follow local data handling policies.

Risk: The skill requires a Baidu API key stored in agent configuration.

Mitigation: Keep BAIDU_API_KEY private, restrict access to the OpenClaw configuration, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyafeichina/skills/baidu-chinese-search)
- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results or plain-text status and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; count is limited to 1-50 results; freshness accepts date ranges or pd, pw, pm, and py shortcuts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
