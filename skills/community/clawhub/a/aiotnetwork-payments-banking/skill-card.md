## Description: <br>
Fund wallets, transfer money, send remittances, and convert currencies. Includes top-up via multiple payment methods and international money transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check balances, top up wallets, transfer money, send international remittances, manage recipients, convert currencies, and retrieve transaction records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Money-moving actions can initiate transfers, remittances, conversions, top-ups, or recipient deletion, and the security evidence says the artifact does not show a clear confirmation step before irreversible actions. <br>
Mitigation: Require the agent to restate amount, currency, recipient, destination, fees, and action type before any transfer, conversion, top-up, remittance, or recipient deletion, and confirm in the payment provider UI where possible. <br>
Risk: Transfer, remittance, and conversion confirmations require sensitive transaction PINs. <br>
Mitigation: Ask for the transaction PIN fresh for each confirmation and never cache, log, or persist PINs, bearer tokens, passwords, card numbers, or CVVs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-payments-banking) <br>
- [Publisher profile](https://clawhub.ai/user/D9m1n1c) <br>
- [Default AIOT payment API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with endpoint descriptions and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL for API base URL configuration; financial operations require authentication and some confirmations require a fresh transaction PIN.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
