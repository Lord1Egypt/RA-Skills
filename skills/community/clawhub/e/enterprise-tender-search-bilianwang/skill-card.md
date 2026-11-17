## Description:

帮助采购与投标团队检索招标和中标公告、分析企业与供应商，并开展采购寻源和市场统计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

采购与投标团队可用它按关键词、地区、金额和时间查找招标项目，查看企业资质与中标记录，并分析供应商、采购方和市场价格。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional automatic signup sends a reusable device identifier; the provider's server-side retention and deletion practices were not verified.

Mitigation: Prefer a manually obtained API key. Before automatic signup, ask the provider how it retains and deletes the device identifier.

Risk: Business search terms are sent to Zhiliaobiaoxun, and some queries consume account credits.

Mitigation: Tell the user what query will be sent and whether it may incur credits; make only the requested lookups and report applicable costs.

Risk: A saved API key or generated login link could expose account access if shared or logged.

Mitigation: Keep API keys and generated login links private; do not include them in user-facing results or logs.

## Reference(s):

- [标讯搜索接口说明](artifact/references/api-search.md)
- [企业分析接口说明](artifact/references/api-company.md)
- [工商信息查询说明](artifact/references/api-registry.md)
- [市场分析接口说明](artifact/references/api-market.md)
- [账户查询接口说明](artifact/references/api-account.md)
- [知了标讯技能文档](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and tables, with links to matching notices when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some searches and company lookups consume account credits; the skill reports costs and limits when relevant.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
