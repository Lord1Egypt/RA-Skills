## Description:

抖音公开数据分析工具，支持关键词搜索、作品与评论抓取、博主作品分析和实时热榜查询，并返回结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容运营、品牌与数据分析人员可用它检索抖音公开内容、查看作品和评论指标、跟踪热点，并为选题、竞品分析和舆情研判整理结构化数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording could send unrelated search terms to a third-party data API; the security review also reports that some components were only partially inspected.

Mitigation: Run it only for a relevant Douyin data request, confirm the keyword or link before querying, and review the skill behavior before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-hot-title-creation)
- [Guaikei service and access information](https://www.guaikei.com)
- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise Markdown summaries when interpreting results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Douyin data; result fields and available counts depend on the query and service plan.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
