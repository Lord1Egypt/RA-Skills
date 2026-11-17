## Description:

从抖音公开内容中检索视频、图文、作品详情、创作者作品、评论和热榜，并输出结构化数据以支持评论洞察与用户反馈分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容运营、市场研究和客服团队可用它追踪热点、比较公开作品，并从评论中归纳用户问题、购买顾虑和反馈，供内部分析与报告使用。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and Douyin links are sent to the third-party guaikei.com API using an API token.

Mitigation: Review the provider’s pricing and privacy terms before use, keep GUAIKEI_API_TOKEN private, and remove saved logs when they are no longer needed; provider retention behavior has not been verified.

## Reference(s):

- [需求挖掘指南](artifact/references/demand-mining.md)
- [命令参数说明](artifact/references/options.md)
- [更新日志](artifact/references/changelog.md)
- [服务与令牌信息](https://www.guaikei.com)
- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/douyin-comment-consumer-insights)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [结构化 JSON 数据与简洁的文本分析总结]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [可供后续分析的抖音公开内容、作品互动和评论数据；痛点归纳须遵循样本说明与证据要求。]

## Skill Version(s):

1.4.2 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
