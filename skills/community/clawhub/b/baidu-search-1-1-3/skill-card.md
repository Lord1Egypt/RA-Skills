## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run live Baidu web searches for current information, documentation, and research topics from an OpenClaw environment configured with a Baidu API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu and may consume Baidu API quota. <br>
Mitigation: Use the skill only for queries appropriate to send to Baidu, monitor quota usage, and use a dedicated API key where possible. <br>
Risk: The BAIDU_API_KEY could be exposed through source control, shared logs, or broad local configuration access. <br>
Mitigation: Keep the key out of source control and shared logs, restrict access to the OpenClaw configuration file, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results printed to stdout, with Markdown setup and command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count from 1 to 50, and optional freshness filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact _meta.json reports 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
