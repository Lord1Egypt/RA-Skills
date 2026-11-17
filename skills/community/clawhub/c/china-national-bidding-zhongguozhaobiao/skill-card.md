## Description:

提供招标采购公告、企业与供应商分析、商机发现和市场数据查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, sales, and market research teams can use the assistant to find Chinese tender and award notices, examine companies and suppliers, and summarize procurement market trends and opportunities.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Automatic registration can collect platform, architecture, and a hashed device identifier; the provider's retention and linkage practices are not established by the supplied artifact.

Mitigation: Set your own ZLBX_API_KEY to bypass device collection, or ask the provider to clarify retention and linkage before accepting automatic registration.

Risk: Search criteria are sent to Zhiliaobiaoxun and queries may consume credits; saved API keys and login links are sensitive.

Mitigation: Limit searches to the user's request, explain when calls may use credits, and keep API keys and login links private.

## Reference(s):

- [Bid search API guidance](references/api-search.md)
- [Company analysis API guidance](references/api-company.md)
- [Company registry data and interpretation guidance](references/api-registry.md)
- [Market analysis API guidance](references/api-market.md)
- [Account API guidance](references/api-account.md)
- [Credential and registration guidance](references/auto-register.md)
- [ClawHub release page](https://clawhub.ai/zhiliaobiaoxun/skills/china-national-bidding-zhongguozhaobiao)
- [Zhiliaobiaoxun API v2](https://mcp-server.zhiliaobiaoxun.com/api_v2/)

## Skill Output:

**Output Type(s):** [Text, Analysis, Markdown]

**Output Format:** [Chinese text summaries and Markdown tables with linked source records when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested filters and available provider data; some successful queries consume credits.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
