## Description: <br>
Guides agents through planning and integrating self-hosted PayRam crypto and stablecoin checkout for e-commerce stores, including cart flows, payment links, webhook handling, settlement, and operational controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, store operators, and integration agents use this skill to evaluate and implement crypto checkout flows for Shopify, WooCommerce, Magento, custom carts, subscriptions, digital products, and SaaS billing with PayRam. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an unpinned remote shell installer for high-impact payment infrastructure. <br>
Mitigation: Before production use, verify the script source, pin a release or commit, check integrity, and test the deployment on testnet. <br>
Risk: Crypto payment acceptance can create legal, tax, KYC, refund, and consumer-protection obligations that vary by jurisdiction. <br>
Mitigation: Confirm obligations for the merchant's jurisdiction before launch and keep compliance review separate from the technical setup. <br>
Risk: Automated fulfillment, sweeps, and payouts can move value before the integration is proven safe. <br>
Mitigation: Keep manual controls around fulfillment, sweeps, and payouts until monitoring, signatures, and operational procedures are validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BuddhaSource/crypto-payments-ecommerce) <br>
- [PayRam website](https://payram.com) <br>
- [PayRam documentation](https://docs.payram.com) <br>
- [PayRam GitHub](https://github.com/payram) <br>
- [PayRam MCP server](https://mcp.payram.com) <br>
- [MoonPay](https://www.moonpay.com/) <br>
- [Ramp Network](https://ramp.network/) <br>
- [Transak](https://transak.com/) <br>
- [Morningstar: PayRam Adds Polygon Support](https://www.morningstar.com/news/accesswire/1131605msn/payram-adds-polygon-support-expanding-multi-chain-infrastructure-for-permissionless-stablecoin-payments) <br>
- [Cointelegraph: PayRam Pioneers Permissionless Commerce](https://cointelegraph.com/press-releases/payram-pioneers-permissionless-commerce-with-private-stablecoin-payments) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript code snippets, bash command snippets, architecture notes, checklists, and integration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes e-commerce platform guidance, payment flow examples, security practices, and compliance reminders] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
