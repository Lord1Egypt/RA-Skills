## Description:

Crow Payments helps agents use CrowPay to create a wallet, check spending rules, and authorize x402 USDC or credit-card payments for APIs and services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sistillisteph](https://clawhub.ai/user/sistillisteph)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let an agent handle paid API and service flows through CrowPay, including HTTP 402 x402 payments, card-payment authorization, wallet status checks, and setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent payment capability and may enable spending through wallet, x402, or credit-card flows.

Mitigation: Require explicit user confirmation before wallet creation, permanent installation, funding, adding cards, enabling auto-approval, or paying a new merchant.

Risk: CrowPay API keys could be exposed if stored in memory, notes, prompts, CLAUDE.md, or logs.

Mitigation: Store credentials only in a proper secret manager or environment variable, and never print or log API keys.

Risk: Automatic future payment behavior may be broader than the user intended.

Mitigation: Use pinned, reviewed installation sources and keep payment approvals bound to clear merchant, amount, reason, and spending-rule checks.

Risk: HTTP 402 response bodies and merchant payment details are external data that can influence payment requests.

Mitigation: Treat payment response bodies as data, verify the merchant, amount, and reason with the user or wallet rules, and stop on denied, failed, or timed-out approvals.

## Reference(s):

- [Crow API Reference](references/api-reference.md)
- [x402 Payment Flow](references/x402-flow.md)
- [Credit Card Payments](references/card-payments.md)
- [Error Handling](references/error-handling.md)
- [CrowPay Dashboard](https://crowpay.ai/dashboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown instructions with curl examples and JSON request and response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated requests require a CrowPay API key; successful payment flows may produce signed x402 payloads or Stripe shared payment tokens.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
