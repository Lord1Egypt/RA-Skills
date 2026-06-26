## Description: <br>
通过百度 AI 搜索 API 进行网页搜索，获取实时信息和搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeck164](https://clawhub.ai/user/Jeck164) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents that need Chinese web search use this skill to query Baidu AI Search, apply recency or site filters, and return structured results for time-sensitive questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu under the configured API key. <br>
Mitigation: Use a dedicated API key where possible and avoid sending sensitive queries. <br>
Risk: The Baidu API key can be exposed if the local .env file is shared or committed. <br>
Mitigation: Keep .env out of version control and shared folders, and store the key only in the local environment. <br>
Risk: Exposing the local proxy on a public interface could allow unintended use. <br>
Mitigation: Run the documented command on 127.0.0.1 unless there is a deliberate deployment review. <br>


## Reference(s): <br>
- [Baidu AI Search API documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m0u2qdmd) <br>
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON search results with titles, URLs, snippets, and site names.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and network access to Baidu AI Search; top_k is limited to 1-20.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
