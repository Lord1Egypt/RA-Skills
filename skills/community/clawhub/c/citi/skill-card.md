## Description: <br>
Financial enablement and accounting skill for agents that need owner-controlled wallets, spending checks, purchase flows, top-up requests, payment links, transaction history, and card checkout workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their human owners use this skill to register and operate a CreditClaw wallet, check spending permissions, make purchases within owner rules, request funding, create payment links, and review transactions. It is most relevant when an agent is intentionally granted controlled financial authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent controlled authority to make real purchases. <br>
Mitigation: Install only when that authority is intentional, require human approval by default, and set tight spending, category, and domain limits. <br>
Risk: Marketplace banking-style branding is not supported by the CreditClaw artifacts. <br>
Mitigation: Verify the CreditClaw operator and any implied bank affiliation independently before relying on the skill. <br>
Risk: CREDITCLAW_API_KEY functions like a payment credential. <br>
Mitigation: Store the key in a secrets manager, send it only to creditclaw.com API endpoints, and rotate it if exposure is suspected. <br>
Risk: Automated heartbeat behavior can prompt top-up requests when balances are low. <br>
Mitigation: Avoid automatic top-up requests and require human confirmation before requesting additional funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jononovo/citi) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill reference](https://creditclaw.com/skill.md) <br>
- [CreditClaw heartbeat reference](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with curl examples and JSON request and response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated calls; financial actions depend on owner-configured limits, approvals, and wallet status.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
