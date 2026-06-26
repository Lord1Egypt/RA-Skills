## Description: <br>
通过 Clawec API 搜索 Ozon 商品，返回价格、销量、评分、市场、链接与图片等。在用户需要 Ozon 搜品、俄罗斯及东欧跨境选品、竞品调研、关键词找货、Ozon 产品搜索时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agents use this skill to search Ozon products through the ClawEC API for product discovery, competitor research, keyword-based sourcing, and Russia or Eastern Europe market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's Ozon search keyword and Clawec API token to clawec.com. <br>
Mitigation: Store CLAWEC_API_KEY in an environment variable or secret manager, avoid sensitive private search terms, and review ClawEC data-handling terms before business use. <br>


## Reference(s): <br>
- [Ozon product search response schema](references/response-schema.md) <br>
- [ClawEC API base](https://www.clawec.com/api) <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-ozon-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional tables, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAWEC_API_KEY for authenticated API calls and returns product fields such as name, price, sales, rating, market, link, and image URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
