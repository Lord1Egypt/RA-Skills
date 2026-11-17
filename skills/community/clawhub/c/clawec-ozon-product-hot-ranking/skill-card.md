## Description:

通过 Clawec API 查询 Ozon 热销产品列表（销量/GMV/价格筛选排序、发货模式、跨境权限、销售水平等）。在用户需要 Ozon 热销商品、爆品榜、单品选品、竞品销量调研、俄罗斯跨境产品榜单时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border ecommerce operators and analysts use this skill to query ClawEC's Ozon hot product ranking API, compare sales, GMV, price, delivery mode, cross-border eligibility, and product-level operating signals, and produce Chinese product selection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Ozon query parameters and the user's CLAWEC_API_KEY to clawec.com.

Mitigation: Use it only when ClawEC API access is intended, keep the API key in the CLAWEC_API_KEY environment variable, and avoid hardcoding or sharing the key.

Risk: Untrusted filtersJson can override documented request fields.

Mitigation: Accept filtersJson only from trusted users or review it before execution, and keep pageSize within the documented API limit.

Risk: Ranking data and generated product-selection observations may be incomplete, stale, or affected by API limits.

Mitigation: Review the returned period, page metadata, and product fields before making commercial decisions.

## Reference(s):

- [ClawEC API Base URL](https://www.clawec.com/api)
- [ClawEC API Key](https://www.clawec.com/api-key?source=q-clawhub)
- [Ozon Hot Product Ranking Endpoint](https://www.clawec.com/api/aigc/ec/ozon/data/product/hot-ranking)
- [Ozon Hot Product Ranking Response Schema](references/response-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-product-hot-ranking)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Chinese Markdown report with product ranking tables, observations, recommendations, and optional bash commands or JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEC_API_KEY for live API access; query pageSize is documented with a maximum of 15.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
