## Description:

Public Zhihu data through DataXAPI: posts, articles, pins (想法), questions, answers, users. 16 endpoints, $0.0020 a call, a failed call is free. Use when the user asks about Zhihu content, accounts, comments or trends, or gives a Zhihu link, ID or account name. 通过 DataXAPI 取知乎的公开数据：帖子、文章、想法、问题、回答、用户。16 个接口，一次 $0.0020，失败不收费。用户问到知乎的内容、账号、评论或热点，或给出知乎的链接、编号、账号名时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve public Zhihu posts, articles, questions, answers, comments, trends, and user information through DataXAPI. It helps an agent select an appropriate Zhihu endpoint and present the returned data with its source and retrieval time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint discovery may send the user's wording to DataXAPI, which may not fit their privacy needs for sensitive queries.

Mitigation: Avoid sending sensitive wording unless DataXAPI's privacy handling meets the user's needs.

Risk: The DataXAPI CLI dependency is unpinned, and the security scan could not resolve local path-like references, so its analysis is partial.

Mitigation: Check how to pin and verify the dataxapi package version before installing; review unresolved references because the scan does not establish that the package is malicious.

## Reference(s):

- [DataXAPI Zhihu API catalog](https://dataxapi.com/apis/zhihu/)
- [DataXAPI Zhihu pricing](https://dataxapi.com/pricing/zhihu/)
- [DataXAPI agent setup instructions](https://dataxapi.com/agents.md)
- [DataXAPI MCP endpoint](https://api.dataxapi.com/mcp)
- [DataXAPI homepage](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-zhihu)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured API response data with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A request returns one page of results; additional pages require additional calls. API calls are billed per endpoint price.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
