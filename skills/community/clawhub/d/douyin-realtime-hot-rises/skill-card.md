## Description:

在用户提供关键词或公开作品、账号链接后，查询抖音公开搜索、热榜、作品与评论数据，并输出供热点选题和内容分析使用的结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、运营、营销和电商团队可用它发现抖音热点与选题，检索公开作品和作者数据，并查看指定作品的详情或评论。结果可用于内容策划、竞品比较和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a benign verdict, but its review is incomplete: 24 of 42 components were fully inspected and tool-misuse analysis was degraded.

Mitigation: Review the uninspected components and tool behavior before installation; treat the scan as incomplete rather than a safety guarantee.

Risk: User-provided search terms and links are sent to the third-party Guaikei API.

Mitigation: Confirm the user is authorized to share the query information and avoid sending sensitive or private data.

Risk: The skill requires an API token to access the service.

Mitigation: Keep GUAIKEI_API_TOKEN in a protected environment variable and out of prompts, shared logs, and command history.

## Reference(s):

- [使用说明](SKILL.md)
- [参数说明](references/options.md)
- [评论需求挖掘指南](references/demand-mining.md)
- [更新日志](references/changelog.md)
- [服务与令牌帮助](https://www.guaikei.com)
- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/douyin-realtime-hot-rises)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON with concise Markdown summaries or tables when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14+ and a Guaikei API token; request limits depend on the plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, changelog; released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
