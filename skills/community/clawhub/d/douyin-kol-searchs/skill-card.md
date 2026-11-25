## Description:

抖音公开数据查询助手，可搜索视频与创作者、查看热榜和作品详情，并获取评论以支持内容与竞品分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、品牌与市场分析人员可按关键词查找抖音视频和达人、跟踪热点，并审阅指定账号或作品的公开数据与评论，以支持选题、竞品观察和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links or IDs are sent to the named third-party API.

Mitigation: Use public data only, avoid including sensitive information in queries, and confirm the service is appropriate for the intended use.

Risk: Account and video-detail lookups can retrieve additional creator or content information.

Mitigation: Request only the records needed for the analysis and keep use within the documented personal or team analysis scope.

## Reference(s):

- [抖音KOL对标账号 ClawHub 页面](https://clawhub.ai/why20261/skills/douyin-kol-searchs)
- [服务网站与 API 开通信息](https://www.guaikei.com)
- [选项与参数参考](references/options.md)
- [输出契约](references/contract.md)
- [错误处理参考](references/errors.md)
- [需求挖掘指南](references/demand-mining.md)
- [公域获客指南](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results summarized as concise text or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data returned by the service; result counts depend on the selected command and token plan.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
