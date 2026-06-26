## Description: <br>
Enables agents to browse For the Cult products, create customer-approved orders with multi-chain payments, and track order status and shipment updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bythecult](https://clawhub.ai/user/bythecult) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users can have an agent shop For the Cult: search products, compare options, prepare checkout details, request approval for payment instructions, and track orders. <br>

### Deployment Geography for Use: <br>
Global, subject to the store's supported shipping countries. <br>

## Known Risks and Mitigations: <br>
Risk: This skill can initiate real shopping and crypto payment flows, and payment or order-recovery steps may be high impact if performed without user approval. <br>
Mitigation: Require the agent to show the cart, total, shipping details, payment chain and token, payment destination, and delivery address for user approval before checkout or payment instructions. <br>
Risk: Automatic error recovery could change purchase, payment, identity, or wallet details without the user noticing. <br>
Mitigation: Do not allow automatic recovery to change purchase, payment, identity, or wallet details; ask the user before retrying any state-changing or sensitive step. <br>
Risk: Optional wallet addresses and identity headers can expose sensitive identity or on-chain associations. <br>
Mitigation: Use wallet addresses and X-Moltbook-Identity only when the user or agent runtime explicitly provides them for the documented purpose, and do not infer or generate identity tokens. <br>


## Reference(s): <br>
- [For the Cult Store](https://forthecult.store) <br>
- [For the Cult API](https://forthecult.store/api) <br>
- [For the Cult API — Agentic Commerce Endpoint Reference](references/API.md) <br>
- [Checkout Request Body — POST /checkout](references/CHECKOUT-FIELDS.md) <br>
- [Error Handling Reference — Agentic Commerce Recovery](references/ERRORS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown guidance with JSON API request and response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and an HTTP client; normal browsing, checkout, and order status do not require API keys.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
