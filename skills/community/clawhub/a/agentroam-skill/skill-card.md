## Description:

Buy travel eSIM data plans, gift cards, and mobile airtime with crypto through AgentRoam, with payment from the user's own wallet and delivery by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adiny](https://clawhub.ai/user/adiny)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and purchase travel eSIM plans, gift cards, and prepaid mobile top-ups using supported crypto payment methods. The skill supports product search, live pricing, order validation, order creation after explicit approval, and order status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved purchases can create real AgentRoam orders and require payment from the user's own wallet.

Mitigation: Require the validation summary and explicit user approval before creating an order, and make the payment amount, network, wallet address, and delivery email clear before the user pays.

Risk: Hotel or flight cross-link suggestions are publisher-provided referrals, not neutral travel recommendations.

Mitigation: Present cross-links as optional referrals and keep the skill focused on connectivity, gift cards, and mobile top-ups.

Risk: Live product prices, coverage, and order states can change.

Mitigation: Use the AgentRoam tools for current product data and order status instead of relying on remembered prices or availability.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/adiny/agentroam-skill)
- [ClawHub skill listing](https://clawhub.ai/adiny/skills/agentroam-skill)
- [AgentRoam MCP endpoint](https://agentroam.ai/api/mcp)
- [AgentRoam MCP discovery manifest](https://agentroam.ai/.well-known/mcp.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with tool-use instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live product data, crypto payment details, order status links, and user confirmation prompts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
