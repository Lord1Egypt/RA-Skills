## Description:

工程建设招投标分析-建设通，当搜索词包含工程、施工、建筑、市政、监理、设计等建筑业专属词汇时触发，聚焦工程项目金额、中标单位资质背景，重点提取建筑类项目核心字段并进行业绩汇总。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkuycl](https://clawhub.ai/user/pkuycl)

### License/Terms of Use:

MIT-0

## Use Case:

Construction sector analysts and business teams use the skill to search tender and award notices, review project amounts and bidder qualifications, and summarize construction project records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender searches send search terms to Zhiliaobiaoxun, and successful data-bearing queries may consume paid credits.

Mitigation: Query only the information needed, review the stated per-call or per-page costs, and check the account balance when useful.

Risk: Optional automatic registration sends a MAC-derived device hash; the evidence does not establish how long it is retained.

Mitigation: Use an existing API key or manual registration to avoid device collection, and approve automatic registration only after reviewing its disclosure.

Risk: A saved API key or temporary login link could expose access to the service account.

Mitigation: Protect the API key and avoid sharing temporary login links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pkuycl/skills/construction-tender-analyzer-jianshetong)
- [Zhiliaobiaoxun skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Tender search API guidance](references/api-search.md)
- [Company analysis API guidance](references/api-company.md)
- [Market analysis API guidance](references/api-market.md)
- [Company registry data guidance](references/api-registry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise Chinese-language summaries and tables in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query-dependent tender results, project amounts, company qualification details, and aggregated performance summaries.]

## Skill Version(s):

1.0.11 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
