## Description: <br>
Searches Florist One products and helps agents price, place, and track flower, balloon, or fruit basket delivery orders through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill through AgentPMT to browse Florist One arrangements, calculate full pricing, schedule delivery, and place or review flower, balloon, and fruit basket orders. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: Recipient and order details are shared with a third-party flower-ordering service for fulfillment. <br>
Mitigation: Use the skill only for explicit flower-delivery requests, review recipient details with the user, and confirm before submitting personal or order data. <br>
Risk: The place_order action can initiate a payment request and order workflow. <br>
Mitigation: Call get_order_total first, confirm the total and delivery date with the user, and rely on mobile app approval before fulfillment. <br>
Risk: Retries could create duplicate order attempts. <br>
Mitigation: Use an idempotency_key when retrying place_order. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/flower-fruit-basket-balloon-delivery) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [AgentPMT mobile app download](https://www.agentpmt.com/download-mobile-app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AgentPMT account setup; payment approval occurs in the mobile app before fulfillment.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
