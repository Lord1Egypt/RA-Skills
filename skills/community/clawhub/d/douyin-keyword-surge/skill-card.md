## Description:

为短视频运营与分析任务查询抖音公开内容，包括关键词搜索、热榜、作者作品、作品详情与评论，并返回结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External short-video operators and analysts use the skill to find public Douyin content, monitor creator activity and trends, and summarize engagement or comment themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, links, or identifiers supplied to the skill are sent to an external API.

Mitigation: Use public content and avoid submitting sensitive identifiers; account for this data transfer before running a query.

Risk: The security scan is partial, so its benign verdict does not cover every file or behavior.

Mitigation: Review the commands you plan to use and their data handling before installation or execution.

Risk: The scanner notes an undeclared account-search capability and does not establish the advertised weekly ranking.

Mitigation: Use account search only when needed and verify ranking results before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-keyword-surge)
- [API access and support](https://www.guaikei.com)
- [Options and command guide](references/options.md)
- [Output contract](references/contract.md)
- [Errors and retry guidance](references/errors.md)
- [Comment demand analysis](references/demand-mining.md)
- [Comment-based customer acquisition](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON results with optional Markdown summaries or analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14+ and GUAIKEI_API_TOKEN. Queries are sent to an external API; result files may be saved locally.]

## Skill Version(s):

1.5.0 (source: artifact frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
