## Description:

提供抖音公开内容搜索、作品与评论查询、博主作品查看及实时热榜数据，并以结构化 JSON 返回结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

短视频运营、内容分析、品牌和客服团队可用它检索抖音公开内容、跟踪热点与对标账号，并查看作品互动和评论。调用前需配置服务令牌；用户提供的关键词或链接会发送给第三方数据服务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills.

Mitigation: Review and scan skill before deployment.

## Reference(s):

- [命令选项参考](references/options.md)
- [评论需求挖掘指南](references/demand-mining.md)
- [ClawHub 发布页](https://clawhub.ai/why20261/skills/douyin-trend-data-track)
- [GuaiKei 数据服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [JSON response envelope containing structured Douyin search, creator, post, comment, or trending data; agents can summarize it as analysis or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One response envelope per query. Fields vary by command and may include titles, creators, engagement counts, labels, comments, and links.]

## Skill Version(s):

1.4.2 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
