## Description: <br>
Shop in any store with any payment method. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creditclaw](https://clawhub.ai/user/creditclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use CreditClaw to let agents register with CreditClaw, check spending permissions, request purchase approval, complete merchant checkout flows, manage storefront payments, and use x402 wallet payments under owner-controlled guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live purchasing authority and storefront payment capabilities. <br>
Mitigation: Use approval_mode ask_for_everything, set low transaction and period limits, restrict allowed domains and categories, monitor the CreditClaw dashboard, and freeze or revoke access if behavior is unexpected. <br>
Risk: The skill uses a CREDITCLAW_API_KEY and includes card-handling flows that could expose payment authority if mishandled. <br>
Mitigation: Store the API key and encrypted card data only in a secure secrets manager, send the key only to creditclaw.com, prefer plugin-based card fill, and avoid legacy or raw card handling where possible. <br>
Risk: Checkout failures, approvals, webhooks, or challenge flows can leave purchase state ambiguous. <br>
Mitigation: Require owner approval before spending, confirm checkout status through CreditClaw, verify webhook signatures when webhooks are used, and stop on CAPTCHA, 3DS, OTP, or unexpected payment errors. <br>


## Reference(s): <br>
- [CreditClaw ClawHub page](https://clawhub.ai/creditclaw/creditclaw) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>
- [Main skill instructions](artifact/SKILL.md) <br>
- [Checkout guide](artifact/CHECKOUT-GUIDE.md) <br>
- [OpenClaw plugin checkout guide](artifact/agents/OPENCLAW.md) <br>
- [OpenClaw legacy sub-agent checkout guide](artifact/agents/OPENCLAW_legacy.md) <br>
- [Stripe x402 wallet guide](artifact/STRIPE-X402-WALLET.md) <br>
- [Webhook guide](artifact/WEBHOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation; normal operation may call CreditClaw APIs and browser checkout tools.] <br>

## Skill Version(s): <br>
2.9.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
