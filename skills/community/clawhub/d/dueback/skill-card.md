## Description:

Dueback: outcome-based bill negotiation. Detect negotiable bills, fees, and purchases; Dueback's backend negotiates and verifies savings against bank data. Free to try — pay only on verified savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunrossmai-rgb](https://clawhub.ai/user/dunrossmai-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to identify potentially negotiable bills, fees, subscriptions, or purchases and, with their explicit approval, submit a case to Dueback for negotiation and savings verification. It also helps users understand applicable fees and manage optional recurring-charge scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting bank accounts shares financial data for savings verification, and optional scans can continue across current and future connected accounts until revoked.

Mitigation: Review Dueback's fees and privacy terms before connecting accounts; grant optional scans only after considering their scope, and revoke consent to stop future scans.

Risk: A prefilled five-star review suggestion may not reflect the user's experience.

Mitigation: Edit the suggested rating and text to match the user's view, or skip the review.

## Reference(s):

- [Dueback connection guide](https://dueback.co/connect.html)
- [Dueback MCP server](https://api.dueback.co/mcp/)
- [ClawHub skill release](https://clawhub.ai/dunrossmai-rgb/skills/dueback)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls]

**Output Format:** [Conversational guidance and structured API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests and optional account scans require user approval; the skill does not negotiate directly or guarantee savings.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
