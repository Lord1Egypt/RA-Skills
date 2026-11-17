## Description:

通过百度 AI 搜索 API 进行网页搜索，获取实时信息和搜索结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeck164](https://clawhub.ai/user/jeck164)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Chinese web content through Baidu AI Search, including current information, site-filtered results, and recency-filtered searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Baidu-backed search proxy can become an unauthenticated service backed by the user's Baidu API key if exposed beyond localhost.

Mitigation: Keep the service bound to 127.0.0.1 and do not expose port 8001 publicly.

Risk: BAIDU_API_KEY is required for operation and could be leaked through committed environment files or careless secret handling.

Mitigation: Store the key in local environment configuration, protect the .env file, and avoid committing secrets.

Risk: Logs and request handling may include submitted search queries or request content.

Mitigation: Treat service logs as sensitive and avoid submitting confidential information as search queries.

## Reference(s):

- [Baidu AI Search documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/2m0u2qdmd)
- [Baidu Qianfan application console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
- [ClawHub skill page](https://clawhub.ai/jeck164/skills/baidu-search-cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search responses and Markdown setup guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and a local FastAPI service; search result count is constrained by top_k from 1 to 20.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
