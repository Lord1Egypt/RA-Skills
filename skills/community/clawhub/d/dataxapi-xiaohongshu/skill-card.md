## Description:

Public Xiaohongshu (RedNote) data through DataXAPI: videos, notes, images, topics, users, comments, PGY, Xiaohongshu Shop. 30 endpoints, $0.0200 to $0.0400 a call, a failed call is free. Use when the user asks about Xiaohongshu (RedNote) content, accounts, comments or trends, or gives a Xiaohongshu (RedNote) link, ID or account name. 通过 DataXAPI 取小红书的公开数据：视频、笔记、图片、话题、用户、评论、蒲公英、小红书商城。30 个接口，一次 $0.0200 到 $0.0400，失败不收费。用户问到小红书的内容、账号、评论或热点，或给出小红书的链接、编号、账号名时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve public Xiaohongshu (RedNote) notes, accounts, comments, trends, creator marketplace data, and shop information. The agent selects an appropriate DataXAPI endpoint, observes per-call pricing, and summarizes returned data with its source and retrieval time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends query wording to DataXAPI when making external requests.

Mitigation: Avoid including sensitive or confidential details in query wording.

Risk: The package is unpinned, creating uncertainty about which package version will run.

Mitigation: Review the package version and pin a release you trust before installation.

Risk: The security scan was partial and does not establish that the skill is safe.

Mitigation: Review the package and its behavior before installation.

## Reference(s):

- [DataXAPI homepage](https://dataxapi.com)
- [Xiaohongshu API reference](https://dataxapi.com/apis/xiaohongshu/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [Xiaohongshu API pricing](https://dataxapi.com/pricing/xiaohongshu/)
- [ClawHub skill listing](https://clawhub.ai/data-x-api/skills/dataxapi-xiaohongshu)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured API data with concise Markdown summaries and source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results; endpoint calls cost $0.02 to $0.04 each, while endpoint discovery and pricing lookup are free.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
