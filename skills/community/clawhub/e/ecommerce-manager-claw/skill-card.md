## Description:

Manage ecommerce store backends in real time via their APIs across Shopify, WooCommerce, BigCommerce, Wix, PrestaShop, Adobe Commerce (Magento), Amazon SP-API, Etsy, and Shopware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

External users and store operators use this skill to inspect and manage ecommerce inventory, orders, products, and customer records through supported platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide powerful ecommerce credentials in chat.

Mitigation: Use only stores you control, prefer read-only or narrowly scoped tokens, avoid pasting admin secrets or refresh tokens into normal chat, and revoke or rotate temporary credentials after use.

Risk: The skill can change live ecommerce data such as inventory, products, orders, fulfillment status, and customer records.

Mitigation: Test on a sandbox store first and require explicit confirmation before any write, fulfillment, cancellation, deletion, or customer update action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhishekj9621/skills/ecommerce-manager-claw)
- [Amazon SP-API getting started](https://developer-docs.amazon.com/sp-api/docs/getting-started)
- [Wix API keys](https://manage.wix.com)
- [Etsy developer portal](https://www.etsy.com/developers)
- [Credential Guides](references/credential-guides.md)
- [Shopify API Reference](references/shopify.md)
- [WooCommerce API Reference](references/woocommerce.md)
- [BigCommerce API Reference](references/bigcommerce.md)
- [Wix API Reference](references/wix.md)
- [PrestaShop API Reference](references/prestashop.md)
- [Adobe Commerce (Magento) API Reference](references/magento.md)
- [Amazon SP-API and Shopware API Reference](references/amazon-shopware.md)
- [Etsy API Reference](references/etsy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute ecommerce API calls after collecting platform credentials and user confirmation for write or destructive actions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
