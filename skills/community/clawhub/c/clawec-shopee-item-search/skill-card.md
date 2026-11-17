## Description:

通过 Clawec API 按站点与类目查询 Shopee 商品列表（近30天销量/GMV、价格、本土跨境、优选商城等筛选）。在用户需要虾皮类目搜品、Shopee 商品数据榜、站点选品、销量销售额筛选时使用；关键词搜品请用 clawec-shopee-product-search。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers, ecommerce operators, and agent developers use this skill to query ClawEC for category-based Shopee item rankings and recent sales, GMV, price, shop type, and rating signals. It supports product discovery workflows by turning site, category, and filter inputs into Chinese product-list analysis and selection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-chosen Shopee query parameters and CLAWEC_API_KEY to ClawEC.

Mitigation: Install only when the user trusts ClawEC with those parameters and keep the API key in the CLAWEC_API_KEY environment variable.

Risk: Users may accidentally provide unrelated secrets while configuring or troubleshooting API access.

Mitigation: Request only the ClawEC API key needed for this skill and avoid collecting or hardcoding unrelated credentials.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [Shopee item search endpoint](https://www.clawec.com/api/aigc/ec/shopee/data/item/search)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-item-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional bash command examples and JSON API response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output; API requests require CLAWEC_API_KEY and pageSize is capped at 10.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
