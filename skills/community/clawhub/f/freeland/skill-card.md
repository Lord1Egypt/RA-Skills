## Description: <br>
Agent-first API for wallet, cards, inbox OTP, Mr. Freeman, eSIM, VPN, and crypto invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvismusli](https://clawhub.ai/user/elvismusli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use Freeland to manage a user-owned account for wallet readiness, virtual cards, OTP-backed checkout, connectivity services, Mr. Freeman chat, and USDT invoice collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with FREELAND_API_KEY can operate wallet, card, OTP inbox, connectivity, and invoice workflows for the user's account. <br>
Mitigation: Install only when intentional account access is desired; prefer approval-based mode, set clear spend and service boundaries, and keep API keys, card details, OTPs, and inbox contents scoped to the immediate task. <br>
Risk: Provider readiness, transaction state, KYC gates, geography restrictions, or missing OTPs can make financial and connectivity workflows fail or become ambiguous. <br>
Mitigation: Read current account state, balances, provider status, and transactions before purchases, top-ups, retries, or invoice actions, and treat provider failures and compliance gates as hard boundaries. <br>


## Reference(s): <br>
- [Freeland homepage](https://freeland.land) <br>
- [Freeland ClawHub listing](https://clawhub.ai/elvismusli/freeland) <br>
- [Payment Safety](references/payment-safety.md) <br>
- [Connectivity Workflows](references/connectivity.md) <br>
- [Invoices](references/invoices.md) <br>
- [Freeland API base URL](https://app.freeland.land/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and API route references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FREELAND_API_KEY for authenticated Freeland account operations.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
