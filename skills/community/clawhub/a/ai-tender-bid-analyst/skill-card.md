## Description:

用自然语言查询并分析招投标数据，支持商机研判、企业与竞争对手分析及市场洞察。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要分析招投标市场的业务人员、采购团队和供应商，用于搜索标讯、分析企业与竞争格局，并整理商机和市场洞察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 自动注册会使用持久设备标识进行设备去重，隐私影响可能未在注册提示中充分体现。

Mitigation: 自动注册前查看设备标识披露并取得用户明确同意；用户也可配置现有 API Key 来跳过注册。

Risk: 搜索词和企业名称会发送给知了标讯，付费查询可能消耗账户积分。

Mitigation: 告知用户查询数据的发送对象及可能费用，并仅执行用户需要的查询。

Risk: API Key 和生成的登录链接需要妥善保护。

Mitigation: 将凭证和登录链接保存在私密位置，不在回复中暴露。

## Reference(s):

- [标讯搜索 API 参考](artifact/references/api-search.md)
- [企业分析 API 参考](artifact/references/api-company.md)
- [市场分析 API 参考](artifact/references/api-market.md)
- [账户查询 API 参考](artifact/references/api-account.md)
- [工商数据口径与解读边界](artifact/references/api-registry.md)
- [自动注册流程与隐私说明](artifact/references/auto-register.md)
- [技能使用文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [ClawHub 发布页](https://clawhub.ai/zhiliaobiaoxun/skills/ai-tender-bid-analyst)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [中文自然语言摘要，按需附 Markdown 表格、标讯链接和数据字段]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果依赖平台可用数据；部分查询会消耗账户积分。]

## Skill Version(s):

1.0.10 (source: frontmatter, server release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
