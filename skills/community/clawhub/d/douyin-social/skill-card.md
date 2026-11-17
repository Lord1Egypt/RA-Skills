## Description:

提供抖音公开视频与评论的只读检索，涵盖关键词搜索、热榜、作品详情、博主作品和评论数据，支持选题、竞品与舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、内容策划和市场分析团队可用此技能检索抖音公开内容与互动数据，支持热点选题、竞品观察、评论洞察和舆情跟踪。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan inspected only part of the skill, so its benign verdict does not cover every component.

Mitigation: Review components that were not fully inspected before installing.

Risk: Broad planning queries may send search terms or links to a third-party API.

Mitigation: Keep requests scoped to authorized public data and confirm the query is appropriate to share.

## Reference(s):

- [使用选项](artifact/references/options.md)
- [评论需求挖掘指南](artifact/references/demand-mining.md)
- [更新日志](artifact/references/changelog.md)
- [瓜客官网与 API 服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [结构化 JSON 数据；按需提供简洁的自然语言分析与建议]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果可能同时保存为 JSON 文件；数据范围、条数和时效受 API 套餐与服务限制。]

## Skill Version(s):

1.4.2 (source: artifact/SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
