## Description:

当用户需要从短视频评论区挖掘潜在客户或销售线索时使用本技能——按关键词搜索内容，再用内容ID拉取评论区数据，提取评论者的昵称、唯一标识、地区和需求表达，实现低成本线索挖掘与竞品截流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, including short-video operators, marketers, analysts, and sales teams, can search public Douyin videos and accounts, inspect public comments and trends, and summarize content insights or potential leads. The skill returns structured data for internal analysis and follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is partial and notes that the skill offers features beyond comment-based lead discovery; using it sends search terms or content links and IDs to a third-party service.

Mitigation: Review which features are being used and send only terms, links, or IDs you are comfortable sharing with the service.

## Reference(s):

- [Customer acquisition workflow](references/customer-acquisition.md)
- [Demand mining workflow](references/demand-mining.md)
- [Output format and data contract](references/contract.md)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON with concise summaries or tables for insights and leads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Douyin content and comment data; lead and insight summaries should be grounded only in returned records.]

## Skill Version(s):

1.5.0 (source: frontmatter, changelog, package.json; released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
