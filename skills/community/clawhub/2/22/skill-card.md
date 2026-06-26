## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yannan](https://clawhub.ai/user/yannan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run live Baidu web searches for current information, documentation, and research topics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu's API and may expose sensitive terms. <br>
Mitigation: Avoid secrets, personal data, and confidential project names in queries. <br>
Risk: The skill depends on a BAIDU_API_KEY configured in the agent environment. <br>
Mitigation: Store the key with restrictive permissions and rotate it if it is exposed. <br>
Risk: Live search results can be incomplete, stale, or unsuitable for high-stakes decisions. <br>
Mitigation: Review returned sources and validate important facts before acting on them. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [ClawHub Skill Page](https://clawhub.ai/yannan/22) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results printed to stdout, with Markdown setup guidance and shell command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count from 1 to 50, and optional freshness filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
