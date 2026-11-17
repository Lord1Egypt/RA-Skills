## Description:

Flower, Fruit Basket, Balloon Delivery helps an agent search Florist One products, calculate full order totals, place delivery orders with card messages, and look up orders through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to browse flowers, fruit baskets, and balloon products, confirm pricing and delivery dates, and place AgentPMT-mediated delivery orders. Developers and agents use the included action schemas to call the supported product actions consistently.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: The setup path includes unpinned remote installer commands.

Mitigation: Prefer pinned or ClawHub/OpenClaw-managed installs and avoid running unpinned npx commands in environments with sensitive files or credentials.

Risk: The workflow can place real delivery orders and trigger mobile payment approval.

Mitigation: Confirm the order total, delivery date, recipient details, and payment approval with the user before placing an order.

Risk: The workflow handles recipient personal data.

Mitigation: Keep tool inputs limited to the information required for the order and avoid placing secrets or payment details in prompts or logs.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/flower-fruit-basket-balloon-delivery)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with JSON request examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines six AgentPMT product actions: list_categories, search_products, get_order_total, place_order, get_order, and list_orders.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
