## Description: <br>
Handles invoice creation, payment link generation, payment status tracking, and automated reminders via Stripe API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to create Stripe payment links and invoices, check payment status, send reminders, manage recurring billing, and record payment events for CashClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real financial actions, including refunds, without a built-in confirmation step. <br>
Mitigation: Require explicit human approval before running payment, invoice, subscription, reminder, or refund commands, and do not allow an agent to run refund commands automatically. <br>
Risk: Stripe API credentials and local CashClaw ledger/dashboard files may expose payment access or customer billing records. <br>
Mitigation: Use restricted Stripe API keys where possible, protect configuration files, and periodically delete or secure ~/.cashclaw ledger and dashboard files. <br>
Risk: Automated reminders can contact clients or re-send invoices at the wrong time if the payment state or recipient is wrong. <br>
Mitigation: Review invoice status, recipient, amount, currency, and reminder schedule before sending reminders; pause automation when a client responds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreataide86/cashclaw-invoicer) <br>
- [Stripe Customers API](https://api.stripe.com/v1/customers) <br>
- [Stripe Invoices API](https://api.stripe.com/v1/invoices) <br>
- [Stripe Payment Links API](https://api.stripe.com/v1/payment_links) <br>
- [Stripe Refunds API](https://api.stripe.com/v1/refunds) <br>
- [Stripe Subscriptions API](https://api.stripe.com/v1/subscriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with bash commands, curl examples, and JSON ledger/dashboard examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js, Stripe credentials, and local CashClaw ledger/dashboard files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
