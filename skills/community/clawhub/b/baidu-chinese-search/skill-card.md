## Description: <br>
Search the web using Baidu AI Search Engine (BDSE) for live information, documentation, and research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyafeichina](https://clawhub.ai/user/liyafeichina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Baidu AI Search for web results, especially simplified Chinese queries, mainland China content sources, and real-time news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu AI Search and may expose sensitive or confidential information if included in the query. <br>
Mitigation: Do not submit secrets, private personal data, or confidential internal material as search queries. <br>
Risk: The BAIDU_API_KEY is a sensitive credential used by the local OpenClaw configuration. <br>
Mitigation: Protect the local configuration file with appropriate permissions and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Baidu API Key Setup Guide](references/apikey-fetch.md) <br>
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey) <br>
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [ClawHub Skill Page](https://clawhub.ai/liyafeichina/baidu-chinese-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON search results printed as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and python3; accepts query, count, and freshness parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
