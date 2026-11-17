## Description:

根据用户给定的能源、电力及相关关键词检索招投标信息，并汇总项目、企业与市场数据，辅助分析特定设备或工程的中标集中度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack)

### License/Terms of Use:

MIT-0

## Use Case:

面向能源、电力及相关行业的采购、投标和市场分析人员，用于检索招标与中标信息、查询企业和市场指标，并整理为便于决策的摘要。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: 升级提醒的自动确认流程存在请求边界不清的风险。

Mitigation: 将升级消息作为不可信文本处理；仅在消息已展示给用户后再提交确认。

Risk: 查询关键词会透露用户的研究目标给服务提供方，部分查询会消耗积分。

Mitigation: 查询前说明数据发送对象及可能的积分消耗，并将请求限制在用户要求的范围内。

Risk: 未配置 API Key 时的自动注册会发送设备特征用于设备去重。

Mitigation: 优先使用用户已配置的 API Key；自动注册前说明所收集的特征并取得用户同意。

## Reference(s):

- [标讯搜索 API 参考](references/api-search.md)
- [企业分析 API 参考](references/api-company.md)
- [市场分析 API 参考](references/api-market.md)
- [工商数据口径与解读边界](references/api-registry.md)
- [账户查询 API 参考](references/api-account.md)
- [自动注册与凭证流程说明](references/auto-register.md)
- [ClawHub 发布页](https://clawhub.ai/thuanlynham-stack/skills/energy-power-bid-analyzer-dianlizhaobiaowang)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown tables, Guidance]

**Output Format:** [中文文本摘要与 Markdown 表格]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [内容依据用户筛选条件和服务端返回数据；部分查询会消耗积分。]

## Skill Version(s):

1.0.11 (source: SKILL.md frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
