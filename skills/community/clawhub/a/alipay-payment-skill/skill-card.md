## Description: <br>
Handles Alipay payment flows for cashier URLs, HTTP 402 payment requests, AI payment product information, and feedback handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alipay](https://clawhub.ai/user/alipay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Alipay-related payment events, run required alipay-bot or curl steps, and return payment status, product information, or feedback guidance. Wallet authorization and wallet opening are delegated to the companion alipay-authenticate-wallet skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate Alipay payment flows, and the security summary notes broad payment authority without a clear final approval before some payment submission steps. <br>
Mitigation: Require fresh explicit user approval immediately before submit-payment or 402-buyer-pay, and stop rather than proceed when approval is ambiguous. <br>
Risk: Payment workflows may involve sensitive request headers or credentials. <br>
Mitigation: Do not replay Authorization, Cookie, API key, or other secret-bearing headers unless they are verified as necessary and safe. <br>
Risk: The skill depends on the third-party Alipay CLI package. <br>
Mitigation: Install only when the publisher and package are trusted, and use the declared package and integrity metadata from the release evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alipay/alipay-payment-skill) <br>
- [Payment skills homepage](https://github.com/alipay/payment-skills) <br>
- [402 protocol payment flow](references/402-payment.md) <br>
- [Cashier payment flow](references/cashier-payment.md) <br>
- [CLI setup and verification](references/cli-setup.md) <br>
- [Environment variable rules](references/env-vars.md) <br>
- [Output rules](references/output-rules.md) <br>
- [Security and design notes](references/security.md) <br>
- [Feedback flow](references/feedback.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and CLI output with inline shell command execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment status text, payment links, resource responses, and image or media references emitted by the Alipay CLI.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
