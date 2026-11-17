## Description:

Enables agents to browse and search For the Cult lifestyle, wellness, tech, and gift products, view product details, create checkout orders with supported multi-chain payments, apply eligible CULT token-holder discounts, and track orders from payment to delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bythecult](https://clawhub.ai/user/bythecult)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to browse For the Cult products, compare options, create checkout orders for physical goods, and track payment or shipment status. It is most relevant when a user asks an agent to shop, find gifts, pay with supported crypto rails, or monitor an existing order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create checkout orders and present payment instructions for real physical purchases.

Mitigation: Before checkout or payment, require the agent to show the exact items, total, email, shipping address, payment chain and token, and any wallet address, then obtain explicit user approval.

Risk: Store-provided recovery hints, error suggestions, or action text could steer the agent toward unsafe or unintended behavior.

Mitigation: Treat API suggestions and action text as untrusted display data; only use documented same-host API paths and do not execute suggested commands or follow unrelated links.

Risk: Identity tokens or wallet addresses can expose sensitive agent, user, or on-chain information.

Mitigation: Send identity headers only when the runtime explicitly supplies them for agent-only endpoints, and request wallet addresses only with user consent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bythecult/skills/agentic-commerce-forthecult)
- [For the Cult storefront](https://forthecult.store)
- [For the Cult API base URL](https://forthecult.store/api)
- [For the Cult API endpoint reference](references/API.md)
- [Checkout request fields](references/CHECKOUT-FIELDS.md)
- [Error handling reference](references/ERRORS.md)

## Skill Output:

**Output Type(s):** [text, guidance, API calls, configuration]

**Output Format:** [Markdown or plain text with structured API request and response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and an HTTP client; normal browsing, checkout, and order status flows require no API key or environment variables.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
