## Description:

Searches the web using Baidu AI Search Engine (BDSE) for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feng-aragron](https://clawhub.ai/user/feng-aragron)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send Baidu AI Search queries from an agent workflow and retrieve current web search results, with optional result count and freshness filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu AI Search and may contain sensitive information.

Mitigation: Use the skill only for queries that are appropriate to send to Baidu and avoid confidential or regulated data unless approved for that environment.

Risk: The skill stores BAIDU_API_KEY in a persistent OpenClaw configuration file.

Mitigation: Protect ~/.openclaw/openclaw.json as a sensitive credentials file, restrict access, and avoid syncing or sharing files that include it.

Risk: The search script prints the parsed request body, which can expose query text in logs.

Mitigation: Remove or disable the request-body print before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feng-aragron/skills/baidufeng)
- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API key console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON search results printed to standard output, with Markdown setup guidance in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; accepts query, count, and freshness parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
