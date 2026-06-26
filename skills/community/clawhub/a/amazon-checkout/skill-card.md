## Description: <br>
CreditClaw Amazon helps agents connect to CreditClaw for owner-approved purchasing, wallet checks, payment signing, merchant detection, checkout guidance, and storefront payment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creditclaw](https://clawhub.ai/user/creditclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with CreditClaw, check spending permissions, request owner-approved purchases, execute merchant checkouts, manage wallet/profile/webhook state, and create payment links or storefront assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has privileged payment and commerce automation authority, including purchases, wallet/profile/webhook management, and storefront or payment asset creation. <br>
Mitigation: Install only when intentionally connecting an agent to CreditClaw, use restricted credentials, verify the publisher and backend controls, and require explicit approval for every transaction. <br>
Risk: Payment-card, wallet, API-key, and webhook-secret workflows can expose funds or account control if sensitive values are mishandled. <br>
Mitigation: Store CREDITCLAW_API_KEY and webhook secrets only in a secure secrets manager, send the API key only to creditclaw.com, and never store or log decrypted card data. <br>
Risk: Automated merchant checkout can submit the wrong purchase or confirm an incorrect transaction state. <br>
Mitigation: Confirm the merchant, amount, owner approval status, callback URL, and final transaction result before submitting or confirming purchases. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/creditclaw/amazon-checkout) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation; outputs operational guidance for payment and commerce workflows.] <br>

## Skill Version(s): <br>
2.9.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
