## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bzmtxh](https://clawhub.ai/user/bzmtxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run live Baidu web searches for current information, documentation, or research topics through a configured BAIDU_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu and require a Baidu Cloud API key. <br>
Mitigation: Use a dedicated, revocable API key and only submit queries that are appropriate for Baidu AI Search. <br>
Risk: The API key is configured in the local OpenClaw configuration file. <br>
Mitigation: Protect ~/.openclaw/openclaw.json with restrictive file permissions and avoid syncing or sharing it. <br>
Risk: Bundled artifact metadata does not exactly match the registry metadata. <br>
Mitigation: Verify the listing identity and prefer the server-resolved publisher and release metadata when reviewing the card. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON search references printed to stdout, with plain-text status and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a BAIDU_API_KEY environment variable; accepts query, count, and freshness parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
