## Description:

为内容运营、品牌调研与创作者检索抖音公开视频和图文、热榜、博主作品、作品详情及评论，并返回结构化数据以支持内容研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

面向内容运营人员、品牌调研者和创作者，用于发现抖音内容与热点、比较公开账号和作品表现，并整理评论观点以辅助选题和趋势分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 查询会将用户提供的关键词、链接或内容 ID 发送给第三方 API。

Mitigation: 查询前确认用户接受此数据共享，并仅提交获准分析的公开内容。

Risk: 安全扫描结论为 benign，但仅完整扫描了部分组件，证据覆盖不完整。

Mitigation: 安装前阅读技能的数据共享说明，并审阅本次发布内容。

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/douyin-content-research-v1)
- [服务与令牌配置](https://www.guaikei.com)
- [参数说明](artifact/references/options.md)
- [评论需求挖掘指南](artifact/references/demand-mining.md)
- [更新日志](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Tables, Markdown]

**Output Format:** [结构化 JSON；按需整理为简短分析、比较表或报告。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [仅处理公开内容；运行需要 GUAIKEI_API_TOKEN；查询使用的关键词或链接会发送至第三方 API，部分分享或播放链接可能过期。]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
