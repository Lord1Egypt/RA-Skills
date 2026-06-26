## Description: <br>
FluxA Agent Wallet allows AI agents to use a user's wallet within an approved scope for x402 payments, USDC transfers, agent-to-agent transfers, payment links, AI social gifting, x402 resource discovery and calls, and payment-related one-shot skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpppppp7](https://clawhub.ai/user/cpppppp7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect an agent to a user-approved FluxA wallet, prepare payment mandates, pay x402 resources, send or receive USDC, create payment links, issue agent identity credentials, and manage payment-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds and make purchases under user-approved wallet mandates. <br>
Mitigation: Keep mandates narrow, short-lived, and purpose-specific; verify every recipient, amount, currency, and service before signing. <br>
Risk: Wallet configuration, agent tokens, JWTs, payer emails, wallet records, and card details are sensitive. <br>
Mitigation: Protect the FluxA wallet data directory, avoid revealing card details or tokens in chat, and disclose only the minimum information needed for the payment task. <br>
Risk: Scheduled wallet checks can create recurring wallet monitoring and may use unpinned latest CLI commands. <br>
Mitigation: Enable scheduled checks only when the user explicitly wants them and pin the CLI version for recurring tasks. <br>


## Reference(s): <br>
- [FluxA Agent Wallet Skill](SKILL.md) <br>
- [Mandate Planning Policy](MANDATE-PLANNING.md) <br>
- [x402 Payment Reference](X402-PAYMENT.md) <br>
- [Payout CLI Reference](PAYOUT.md) <br>
- [Payment Link CLI Reference](PAYMENT-LINK.md) <br>
- [Agent Verifiable Credential Reference](VC-ISSUE.md) <br>
- [Scheduled Wallet Check Setup](SCHEDULED-CHECKIN.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cpppppp7/fluxa-agent-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authorization URLs, wallet status summaries, payment identifiers, transaction status, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.4.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
