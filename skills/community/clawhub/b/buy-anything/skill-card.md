## Description: <br>
Purchase products from Amazon and Shopify stores through conversational checkout. Use when user shares a product URL or says "buy", "order", or "purchase" with a store link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsyvic](https://clawhub.ai/user/tsyvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to buy products from Amazon or Shopify store links through a conversational checkout flow that collects shipping details, uses a BasisTheory payment token, submits the purchase through Rye, and reports order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real purchases and is financially sensitive. <br>
Mitigation: Set a spending limit, review the item and total, and require an explicit same-turn confirmation before each order. <br>
Risk: The skill handles shipping details and BasisTheory token IDs, and may save tokens or addresses in agent memory. <br>
Mitigation: Save payment tokens and addresses only after explicit user permission; use a fresh BasisTheory token when memory handling is unclear. <br>
Risk: Checkout depends on external services and store fulfillment through Rye, BasisTheory, Amazon, and Shopify stores. <br>
Mitigation: Install and use the skill only when those services and the store checkout flow are trusted. <br>


## Reference(s): <br>
- [Buy Anything ClawHub Page](https://clawhub.ai/tsyvic/buy-anything) <br>
- [Rye API Documentation](https://docs.rye.com) <br>
- [BasisTheory](https://basistheory.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce purchase status summaries, spending-limit prompts, payment-token handling guidance, and curl-based Rye API requests.] <br>

## Skill Version(s): <br>
3.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
