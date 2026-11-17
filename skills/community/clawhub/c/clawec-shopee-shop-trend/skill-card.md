## Description:

通过 Clawec API 查询 Shopee 店铺趋势（月/季/年颗粒度，销量销售额、动销率、粉丝等时间序列；可按类目过滤）。在用户需要虾皮店铺趋势、竞店走势、店铺经营变化分析时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketplace analysts, and developers use this skill to query Shopee shop trend data from Clawec and produce concise Chinese trend reports covering sales, GMV, active rate, listings, followers, and ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee shop IDs, date ranges, optional category IDs, and the Clawec API key to Clawec to perform trend lookups.

Mitigation: Use the skill only for intended Clawec shop-trend queries, store CLAWEC_API_KEY in the environment, and avoid hardcoding or sharing the key.

Risk: Trend reports may be incomplete if pagination is not handled when the response total exceeds the current page size.

Mitigation: Check total, pageNo, and pageSize in the response and request additional pages when needed before drawing conclusions.

## Reference(s):

- [Shopee shop trend response schema](references/response-schema.md)
- [Clawec API base URL](https://www.clawec.com/api)
- [Shopee shop trend API endpoint](https://www.clawec.com/api/aigc/ec/shopee/data/shop/trend)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-shop-trend)
- [Publisher profile](https://clawhub.ai/user/anyunzhong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON API response and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a Chinese Shopee shop trend report; API requests require CLAWEC_API_KEY and user-supplied site, shop ID, granularity, date range, and optional category and pagination parameters.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
