## Description:

为 AI Agent 提供招投标公告搜索、企业与市场分析，并生成结构化标讯报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement analysts use the skill to search tender and award notices, examine companies and markets, and prepare structured procurement reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic signup can send a persistent device identifier to the provider.

Mitigation: Review the device-data disclosure and require explicit user consent before signup; an existing ZLBX_API_KEY skips device enrollment.

Risk: Queries send search targets to Zhiliaobiaoxun and successful results may consume account credits.

Mitigation: Avoid confidential query terms, request only needed data, and check the account balance before credit-consuming queries when appropriate.

Risk: The provider's server-side data retention and deletion practices are not established by the available materials.

Mitigation: Avoid sending confidential or sensitive search targets unless the provider's handling is acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhiliaobiaoxun/skills/bid-data-intelligent-agent)
- [Bid search API guide](artifact/references/api-search.md)
- [Company analysis API guide](artifact/references/api-company.md)
- [Market analysis API guide](artifact/references/api-market.md)
- [Company registry data guide](artifact/references/api-registry.md)
- [Account API guide](artifact/references/api-account.md)
- [Automatic signup guide](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Structured reports]

**Output Format:** [Text and Markdown, including structured tables and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report detail depends on the requested queries and available records.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
