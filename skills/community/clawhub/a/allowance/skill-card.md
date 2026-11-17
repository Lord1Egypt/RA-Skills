## Description:

Allowance agent purchase wallet. Use when the user asks to buy something, make a purchase, order an item, book travel, reserve something, pay, or spend money on their behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useallowance](https://clawhub.ai/user/useallowance)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request scoped spending approval, issue limited virtual cards, complete checkout, and report purchase outcomes without exposing the user's real card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent real-money checkout authority after user approval.

Mitigation: Use it only with a concrete merchant, item, total cap, and shipping expectations, and require a new approval when the realized total or item materially differs.

Risk: The setup flow installs mutable external CLI code globally.

Mitigation: Prefer pinned and verified versions of both the skill and Allowance CLI before enabling purchase flows.

Risk: Checkout can expose one-time virtual card details inside the browser session.

Mitigation: Type card details directly into merchant forms only and do not paste, summarize, or reveal card number, CVV, expiry, or last four in chat.

## Reference(s):

- [Allowance homepage](https://useallowance.com)
- [Canonical hosted skill file](https://useallowance.com/SKILL.md)
- [ClawHub skill listing](https://clawhub.ai/useallowance/skills/allowance)
- [Publisher profile](https://clawhub.ai/user/useallowance)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires concrete purchase details, an approved spend cap, and local browser control before checkout.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
