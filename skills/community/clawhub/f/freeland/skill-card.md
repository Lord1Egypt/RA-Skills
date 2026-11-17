## Description:

Agent-first API for wallet, cards, inbox OTP, Mr. Freeman, eSIM, VPN, and crypto invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use Freeland to operate a user-owned Freeland account for wallet readiness, virtual cards, OTP-backed checkout, eSIM and VPN service setup, Mr. Freeman chat, and USDT invoice creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad agent access to wallet, card, OTP, purchase, VPN, and invoice actions.

Mitigation: Install only for intended Freeland account use, prefer explicit invocation, and set clear spending, merchant, service, and action limits.

Risk: Sensitive card credentials, OTPs, inbox messages, invoice details, eSIM profiles, or VPN configs may be exposed during account workflows.

Mitigation: Reveal sensitive values only when needed for the active task and avoid retaining or displaying them longer than necessary.

Risk: Financial or service-changing actions can move balances, issue or top up cards, buy connectivity services, activate VPN subscriptions, or create invoices.

Mitigation: Require confirmation before financial or service changes unless the user has provided explicit pre-authorization with clear boundaries.

## Reference(s):

- [Freeland homepage](https://freeland.land)
- [Freeland ClawHub skill page](https://clawhub.ai/elvismusli/skills/freeland)
- [Payment Safety](references/payment-safety.md)
- [Connectivity Workflows](references/connectivity.md)
- [Invoices](references/invoices.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FREELAND_API_KEY for account operations; may surface sensitive account, card, OTP, inbox, invoice, eSIM, or VPN details only when needed for the active task.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
