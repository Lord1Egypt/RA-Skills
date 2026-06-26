## Description: <br>
Daily e-commerce intelligence for Indian Flipkart and Amazon India sellers that tracks orders, returns, inventory levels, competitor pricing, Buy Box status, and sends WhatsApp morning summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utsavs](https://clawhub.ai/user/utsavs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Indian marketplace sellers use this skill to monitor Flipkart seller operations, receive daily WhatsApp summaries, review inventory and pricing alerts, and act on order, shipment, return, and revenue questions. The skill can optionally include Amazon India seller visibility when Amazon SP-API credentials are configured. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live marketplace changes such as price updates or order cancellation. <br>
Mitigation: Use least-privilege seller API credentials and require explicit seller approval before any order, inventory, or pricing change is executed. <br>
Risk: The skill can send seller performance and operations data through WhatsApp or other external channels. <br>
Mitigation: Limit notification fields to necessary business metrics, control recipients, and avoid sending sensitive seller or customer data. <br>
Risk: Optional Amazon India integration expands the account and data surface area. <br>
Mitigation: Enable only the marketplaces needed and configure Amazon SP-API credentials separately with the narrowest permissions available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utsavs/flipkart-seller-dashboard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/utsavs) <br>
- [Flipkart Marketplace Seller API base URL](https://api.flipkart.net/sellers/) <br>
- [Flipkart Seller OAuth token endpoint](https://api.flipkart.net/sellers/oauth-service/oauth/token) <br>
- [Amazon India Selling Partner API endpoint](https://sellingpartnerapi-fe.amazon.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown messages with API examples, cron entries, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLIPKART_APP_ID and FLIPKART_APP_SECRET; AMAZON_SP_API_REFRESH_TOKEN is optional for Amazon India summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
