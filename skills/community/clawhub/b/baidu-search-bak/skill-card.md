## Description: <br>
Search the web using Baidu AI Search Engine (BDSE) for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aysun168](https://clawhub.ai/user/aysun168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Baidu web searches from an agent workflow, with optional result count and freshness filters. It is suited for live information lookup, documentation discovery, and research queries where sending the search terms to Baidu is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu using the configured API key. <br>
Mitigation: Avoid confidential search terms and use the skill only when Baidu search processing is acceptable. <br>
Risk: The Baidu API key may be exposed if the OpenClaw configuration is shared or committed. <br>
Mitigation: Keep ~/.openclaw/openclaw.json private, avoid source-control or synced-backup exposure, and rotate the key if it is exposed. <br>
Risk: Baidu API use may affect account usage or billing. <br>
Mitigation: Use a dedicated API key where possible and monitor Baidu account usage. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API key console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [ClawHub skill page](https://clawhub.ai/aysun168/baidu-search-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count, and freshness parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
