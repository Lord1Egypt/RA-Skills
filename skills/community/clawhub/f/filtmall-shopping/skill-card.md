## Description:

Filtmall Shopping lets agents find and compare live Filtmall products, provide bounded cosmetic-ingredient information, and continue buyer-controlled shopping flows for cart, checkout, orders, logistics, and after-sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filtmall](https://clawhub.ai/user/filtmall)

### License/Terms of Use:

Mixed: Apache-2.0 and LicenseRef-Filtalgo-CLI-Runtime

## Use Case:

External shoppers use this skill through an agent to discover, compare, and buy Filtmall products, then follow up on payment, orders, delivery, refunds, after-sales, and customer-service tasks. It also supports read-only lookup for a single named cosmetic ingredient within stated safety boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign in to Filtmall and read shopping account context such as orders, addresses, logistics, and after-sales records.

Mitigation: Use it only with a trusted Filtmall account context and avoid exposing credentials, device codes, tokens, full addresses, payment credentials, or session identifiers in conversation.

Risk: The skill can perform consequential shopping actions such as changing cart contents, creating checkout or payment links, cancelling orders, and starting after-sales workflows.

Mitigation: Review the specific item, address, amount, order, and action before confirming; execute state-changing actions only after explicit user confirmation.

Risk: Live product, price, stock, order, logistics, and customer-service data may change after the agent response.

Mitigation: Treat current Filtmall service responses and opened pages as the source of truth, and re-check live status before purchase, payment, cancellation, or after-sales decisions.

Risk: Cosmetic ingredient and shopping flows can intersect with allergy or medical-safety concerns.

Mitigation: Stop product or ingredient workflows for severe current symptoms and direct the user to appropriate medical help instead of recommending products or drawing medical conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/filtmall/skills/filtmall-shopping)
- [Filtmall Publisher Profile](https://clawhub.ai/user/filtmall)
- [Official Filtmall Website](https://www.filtalgo.com/)
- [About Filtmall](https://www.filtalgo.com/about)
- [LLM Reference](https://www.filtalgo.com/llms.txt)
- [Machine-Readable Service Directory](https://www.filtalgo.com/agents.json)
- [Product Search](references/product-search.md)
- [Product Followups](references/product-followups.md)
- [Cart, Address, and Checkout](references/cart-address-checkout.md)
- [Orders and Logistics](references/orders-logistics.md)
- [Customer Service and After-Sales](references/customer-service-after-sales.md)
- [Makeup Component Search](references/makeup-component-search.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with structured product, checkout, order, logistics, after-sales, and ingredient summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include buyer-facing authorization, payment, product, order, logistics, after-sales, and customer-service links returned by Filtmall services.]

## Skill Version(s):

1.11.1 (source: evidence.release.version, SKILL.md metadata, CHANGELOG, README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
