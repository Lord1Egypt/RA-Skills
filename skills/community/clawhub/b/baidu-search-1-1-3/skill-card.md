## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve live web search results from Baidu for documentation lookup, current information, and research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires BAIDU_API_KEY, which is a secret credential.

Mitigation: Store the key outside source control, restrict access to the OpenClaw configuration, and rotate the key if it is exposed.

Risk: Search queries are sent to Baidu's external service.

Mitigation: Use the skill only for queries that are acceptable to share with Baidu.

## Reference(s):

- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search API Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [ClawHub Skill Page](https://clawhub.ai/andy27725/skills/baidu-search-1-1-3)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON search results and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a BAIDU_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
