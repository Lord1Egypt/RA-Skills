## Description: <br>
Ecommerce Assistant helps agents research ecommerce products, analyze Shopify competitors, monitor prices, and produce product reports for Amazon, Shopify, and related platforms. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[lhldolike](https://clawhub.ai/user/lhldolike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce researchers, sellers, dropshippers, and developers use this skill to explore product opportunities, compare Shopify stores, track price changes, and generate research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon search results, price alerts, and generated reports may be simulated or stale when real API-backed data collection is not configured. <br>
Mitigation: Treat outputs as research leads only; verify product, price, and margin data against approved live sources before purchasing, pricing, dropshipping, or competitor decisions. <br>
Risk: The price tracking workflow can retain watchlist and price history data locally. <br>
Mitigation: Review and clear ~/.ecommerce-assistant according to your data retention requirements. <br>
Risk: Store analysis can query public Shopify storefront endpoints. <br>
Mitigation: Run analysis only against public stores you are authorized to query and respect platform rate limits and terms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lhldolike/ecommerce-assistant) <br>
- [Amazon API Guide](references/amazon-api.md) <br>
- [Shopify API Guide](references/shopify-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus JSON, CSV, table, or Markdown reports from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ecommerce APIs when configured, query public storefront endpoints, and store watchlist or price history data under ~/.ecommerce-assistant.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
