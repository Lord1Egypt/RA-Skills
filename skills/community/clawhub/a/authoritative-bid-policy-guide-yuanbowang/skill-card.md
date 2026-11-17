## Description:

权威采招政策与标讯指南-元博网，当用户查询大型基础设施项目、重点政企采购或需要基于标讯进行宏观趋势盘点时调用，需调用聚合与分析接口，输出格式严谨、数据翔实的市场简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkuycl](https://clawhub.ai/user/pkuycl)

### License/Terms of Use:

MIT-0

## Use Case:

面向外部用户，按需检索招标采购公告、分析企业与市场数据，并据此整理大型基础设施项目和重点政企采购的市场简报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic signup sends a stable device identifier, and its privacy implications may be understated.

Mitigation: Review the signup disclosure, ask the provider about retention and deletion, or configure your own ZLBX_API_KEY to skip device collection.

Risk: Successful data queries can spend account credits.

Mitigation: Check the account balance and limit queries to the information the user requested.

## Reference(s):

- [标讯搜索接口说明](artifact/references/api-search.md)
- [企业分析接口说明](artifact/references/api-company.md)
- [企业工商数据口径与解读边界](artifact/references/api-registry.md)
- [市场分析接口说明](artifact/references/api-market.md)
- [账户查询接口说明](artifact/references/api-account.md)
- [自动注册与隐私说明](artifact/references/auto-register.md)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Chinese-language market briefs in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query scope follows the user's request; successful data queries may consume account credits.]

## Skill Version(s):

1.0.11 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
