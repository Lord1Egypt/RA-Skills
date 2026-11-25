## Description:

该技能通过关键词搜索、热榜、创作者作品与评论数据获取抖音公开内容，并支持生成舆情与内容分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Marketing, operations, and research teams use the skill to retrieve public Douyin search, creator, post, comment, and trending data for content planning, competitor monitoring, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags account discovery and customer lead gathering beyond the stated monitoring purpose.

Mitigation: Review those workflows before use and limit queries to the public-data tasks you intend to perform.

Risk: Search terms and supplied links or IDs are sent to a third-party API.

Mitigation: Check that the query terms and identifiers are appropriate to share with the service before running a lookup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-sentiment-monitor)
- [Service and token setup](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Error handling](references/errors.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise sentiment, trend, or content-analysis reports in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; query results may be saved in the skill's logs directory.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
