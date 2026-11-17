## Description:

Searches Amazon and TikTok products by keyword through the AlphaShop REST API, with filters for price, sales, rating, listing age, and region.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce operators use this skill to search Amazon and TikTok product listings by keyword, market, and filters for product discovery, selection analysis, market research, and price comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict because credential and network behavior are under-disclosed.

Mitigation: Review before installing, restrict network access as appropriate, and provide AlphaShop credentials only through protected environment configuration.

Risk: Product-search queries, user identifiers, and credentials may be sent to AlphaShop/1688 services.

Mitigation: Use this skill only if the deployment trusts AlphaShop/1688 with those queries and credentials, and avoid command-line secrets.

Risk: Bundled image-search documentation broadens the apparent scope beyond the released keyword product-search client.

Mitigation: Treat image-search capabilities as out of scope until the publisher clarifies or removes the conflicting documentation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/1688aiinfra/skills/alphashop-sel-product-search)
- [Product Search API Reference](artifact/references/api.md)
- [AlphaShop API Credential Management](https://www.alphashop.cn/seller-center/apikey-management)
- [Bundled Image Product Recall API Reference](artifact/references/图片商品召回接口文档.md)
- [Bundled Image Product Recall Technical Design](artifact/references/图片商品召回接口技术设计文档.md)
- [Bundled Image Product Recall Test Plan](artifact/references/图片商品召回接口测试方案.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and optional JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AlphaShop credentials via ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY for authenticated API calls; product results are returned as text and can optionally be written as JSON with --output.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
