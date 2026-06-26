## Description: <br>
Lobster Brew helps your OpenClaw discover coffee roasters, compare coffees, build personalized carts, and hand off a secure Shopify checkout link for you to complete the purchase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abuiles](https://clawhub.ai/user/abuiles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to discover coffee roasters, compare coffee, subscription, and brewing gear options, prepare merchant carts, and return a checkout link for user-controlled payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coffee-shopping queries, cart details, preference information, and selected merchant data may be used with Lobster Brew and the merchant's Shopify MCP service. <br>
Mitigation: Use the skill only when comfortable with that sharing, and clear agent memory if coffee preferences or prior purchases should not be retained. <br>
Risk: Product availability, prices, subscription cadence, checkout terms, and selling-plan support can vary by merchant. <br>
Mitigation: Treat merchant MCP data and Shopify checkout as authoritative, review products, quantities, subscription details, prices, and checkout terms before paying, and stop when a required subscription flow is unsupported. <br>


## Reference(s): <br>
- [Lobster Brew](https://lobsterbrew.com) <br>
- [Buy Coffee on ClawHub](https://clawhub.ai/abuiles/buy-coffee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, guidance] <br>
**Output Format:** [Markdown text with a structured checkout handoff summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes merchant, product, variant, purchase type, selling plan details, cadence, savings summary, checkout URL, and resolution path when available.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
