## Description:

Alipay Payment Skill handles Alipay cashier payments, HTTP 402 protocol payments, AI payment product information, and payment issue feedback for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alipay](https://clawhub.ai/user/alipay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external-facing agents use this skill to route Alipay cashier and HTTP 402 payment flows, present AI payment product information, and collect payment issue feedback. Wallet setup, authorization, and binding are delegated to the separate alipay-authenticate-wallet skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates sensitive payment steps and may proceed after payment intent is inferred.

Mitigation: Require clear user confirmation of payee, amount, and item before any payment command is run.

Risk: The skill may install and execute the Alipay CLI package from npm.

Mitigation: Install only the fixed package version from the trusted publisher and verify the published integrity value before installation.

Risk: The skill forwards payment request details and contextual values needed for payment handling.

Mitigation: Forward only the details required for the active payment flow and avoid sending payment links through channels the user did not choose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alipay/skills/alipay-payment-skill)
- [Payment skills homepage](https://github.com/alipay/payment-skills)
- [Cashier payment flow](references/cashier-payment.md)
- [HTTP 402 payment flow](references/402-payment.md)
- [CLI setup](references/cli-setup.md)
- [Environment variables](references/env-vars.md)
- [Output rules](references/output-rules.md)
- [Image output rules](references/image-output.md)
- [Security design](references/security.md)
- [Feedback flow](references/feedback.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with CLI output, payment links, image references, and shell command execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment URLs, QR image references, wallet status handling, and payment status responses.]

## Skill Version(s):

0.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
