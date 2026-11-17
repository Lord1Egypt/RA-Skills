## Description:

招投标大数据 AI 分析平台，用自然语言完成市场分析、商机研判与趋势预测：多维聚合统计（月/季/年/省份/行业/品牌）、Top采购单位/中标单位/中标品牌、历史中标价格走势、潜在中标候选预测。当用户提出招投标市场分析、行业商机简报、采购趋势、市场份额、谁在买谁在中标等开放式分析需求时，必须使用此SKILL。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and business analysts use this skill to search tender data, compare purchasers, suppliers and brands, review company information, and summarize market trends and opportunities.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Optional automatic signup sends a persistent device fingerprint; the provider's retention and deletion practices were not verified.

Mitigation: Use a preconfigured API key or manual registration to skip fingerprint collection, and review the provider's privacy practices before opting in.

Risk: Search terms are sent to the service, and some successful data lookups consume credits.

Mitigation: Avoid sensitive query terms and check the requested scope and cost before running paid lookups.

Risk: An exposed API key or temporary login link could allow account access.

Mitigation: Store API keys and temporary login links securely; do not share them in chat.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhiliaobiaoxun/skills/ai-bidding-data-platform)
- [Bid search API guide](artifact/references/api-search.md)
- [Company analysis API guide](artifact/references/api-company.md)
- [Market analysis API guide](artifact/references/api-market.md)
- [Company registry data and interpretation guide](artifact/references/api-registry.md)
- [Account API guide](artifact/references/api-account.md)
- [Automatic registration and privacy guide](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Tables]

**Output Format:** [Markdown summaries, comparisons, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected query terms, filters, and available records; some successful lookups consume credits.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
