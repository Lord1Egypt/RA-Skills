## Description: <br>
Manage ecommerce store backends in real time through APIs for inventory, orders, products, and customer workflows across major ecommerce platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abhishekj9621](https://clawhub.ai/user/Abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and ecommerce teams use this skill to retrieve store data and manage stock, orders, products, and customer records through supported platform APIs. The skill is intended for live ecommerce administration, including read operations and approved write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide powerful ecommerce store credentials. <br>
Mitigation: Use narrowly scoped, temporary credentials where possible; avoid long-lived admin secrets; and revoke or rotate credentials after use. <br>
Risk: The skill can change live store data, including orders, products, inventory, fulfillment, and customer records. <br>
Mitigation: Require explicit user approval before every write, delete, fulfillment, cancellation, or customer update and review the intended change before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abhishekj9621/ecommerce-manager-claw) <br>
- [Credential Guides](artifact/references/credential-guides.md) <br>
- [Shopify API Reference](artifact/references/shopify.md) <br>
- [WooCommerce API Reference](artifact/references/woocommerce.md) <br>
- [BigCommerce API Reference](artifact/references/bigcommerce.md) <br>
- [Wix API Reference](artifact/references/wix.md) <br>
- [PrestaShop API Reference](artifact/references/prestashop.md) <br>
- [Adobe Commerce Magento API Reference](artifact/references/magento.md) <br>
- [Amazon SP-API and Shopware API Reference](artifact/references/amazon-shopware.md) <br>
- [Etsy API Reference](artifact/references/etsy.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown guidance with API request details and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed store changes, credential setup steps, API endpoint details, and tabular summaries of store data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
