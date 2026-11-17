## Description:

Helps merchants audit and improve product data and checkout readiness so AI shopping agents can find, understand, and purchase the right variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and ecommerce teams use this skill to audit product feeds, variants, structured product data, shipping and return details, and agent checkout flows, then prioritize repairs that help shopping agents interpret their catalogs accurately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated checkout tests could cause unintended purchases without spending and approval controls.

Mitigation: Use a test storefront with sandbox payments and fulfillment disabled. For production testing, stop before order submission unless the purchase and total cost are explicitly approved, and set spending and order-count limits.

## Reference(s):

- [Source references](artifact/references/sources.md)
- [Google Merchant Center product data specification](https://support.google.com/merchants/answer/7052112)
- [Google product structured data](https://developers.google.com/search/docs/appearance/structured-data/product)
- [Schema.org Product](https://schema.org/Product)
- [Schema.org OfferShippingDetails](https://schema.org/OfferShippingDetails)
- [Schema.org MerchantReturnPolicy](https://schema.org/MerchantReturnPolicy)
- [GS1 GTIN standard](https://www.gs1.org/standards/id-keys/gtin)
- [OpenAI: Buy it in ChatGPT and the Agentic Commerce Protocol](https://openai.com/index/buy-it-in-chatgpt/)
- [OpenAI: Powering Product Discovery in ChatGPT](https://openai.com/index/powering-product-discovery-in-chatgpt/)
- [OpenAI Agentic Commerce product feed specification](https://developers.openai.com/commerce/specs/file-upload/products)
- [Agentic Commerce Protocol](https://www.agenticcommerce.dev/)
- [Worked example: ChatGPT shopping and the Agentic Commerce Protocol (2025–2026)](artifact/examples/chatgpt-shopping-agentic-commerce-protocol-2025-2026.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown checklists and SKU audit tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include measured Seen, Understood, and Bought rates and a prioritized repair list.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
