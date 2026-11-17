## Description:

Search and book real flights with USDC payments across 500+ airlines, including flight comparison, booking, payment, confirmation, and check-in guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobuta23](https://clawhub.ai/user/kobuta23)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search real flight options, compare prices, create bookings, and complete travel workflows paid in USDC on Base. Agents should request explicit approval before sending passenger details or initiating payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send passenger booking details to a third-party API.

Mitigation: Require explicit user approval before transmitting passenger data and share only the details needed to create the selected booking.

Risk: The skill can instruct an agent to make an irreversible USDC payment.

Mitigation: Do not allow unattended wallet transfers; verify the Base network, USDC token, recipient address, exact amount, booking ID, and fees before every transaction, and prefer the hosted checkout URL.

## Reference(s):

- [Cabin source homepage](https://github.com/yolo-maxi/cabin)
- [Cabin API](https://api.cabin.team)
- [Cabin website](https://cabin.team)
- [ClawHub skill page](https://clawhub.ai/kobuta23/skills/cabin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, flight options, booking links, and payment instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rendered PNG flight comparison URLs, booking references, checkout URLs, confirmation URLs, and check-in URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
