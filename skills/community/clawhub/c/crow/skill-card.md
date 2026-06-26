## Description: <br>
Agent payment service via CrowPay - gives an agent a wallet to pay for APIs and services, including HTTP 402 Payment Required flows, API credits, subscriptions, merchant card payments, wallet setup, and spending-rule management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sistillisteph](https://clawhub.ai/user/sistillisteph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent set up and operate CrowPay payment flows for paid APIs, x402 USDC payments, card-based merchant payments, budget checks, and approval polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent real spending authority through CrowPay payment flows. <br>
Mitigation: Install only when agent payments are intended, require explicit confirmation for wallet setup and each new merchant, and validate merchant, domain, amount, and payee before paid calls. <br>
Risk: The CrowPay API key is a secret credential that the artifact asks agents to store persistently. <br>
Mitigation: Store the API key only in a scoped secret manager or environment variable, and avoid writing it into memory, notes, logs, or user-visible output. <br>
Risk: Auto-approval and broad activation could allow unintended payments. <br>
Mitigation: Disable or tightly cap auto-approval and check spending rules and remaining budget before payment authorization. <br>
Risk: The artifact suggests installing extra skills that were not part of this reviewed release. <br>
Mitigation: Do not install suggested extra skills unless they are separately reviewed. <br>


## Reference(s): <br>
- [Crow API Reference](references/api-reference.md) <br>
- [Credit Card Payments](references/card-payments.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [x402 Payment Flow](references/x402-flow.md) <br>
- [CrowPay Dashboard](https://crowpay.ai/dashboard) <br>
- [Crow Payments on ClawHub](https://clawhub.ai/sistillisteph/crow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline curl commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce payment setup, authorization, polling, status-check, and settlement instructions that require secret handling and user confirmation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
