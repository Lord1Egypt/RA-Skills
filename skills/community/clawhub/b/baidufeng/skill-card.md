## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feng-aragron](https://clawhub.ai/user/feng-aragron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run live Baidu AI Search queries for current information, documentation, and research topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu's AI Search API. <br>
Mitigation: Install only when that data flow is acceptable, and avoid sending sensitive search terms. <br>
Risk: The skill requires a BAIDU_API_KEY and setup guidance allows storing it in the OpenClaw configuration file. <br>
Mitigation: Keep the key secret, prefer environment or managed secret storage when available, and protect ~/.openclaw/openclaw.json if the key is stored there. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON search results with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and supports query, count, and freshness request parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
