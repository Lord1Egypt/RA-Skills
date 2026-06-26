## Description: <br>
CardZero is a payment wallet skill for AI agents that can create USDC wallets on Base L2, make payments, pay x402 paywalls, check balances, view transactions, and run A2A jobs with on-chain escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrocker](https://clawhub.ai/user/mrocker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent manage a CardZero USDC wallet, pay supported services, send payments to other agents, and coordinate A2A job escrow while staying within owner-set spending rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use CardZero credentials to send USDC and initiate payment or escrow flows. <br>
Mitigation: Install only when payment capability is intended, use a dedicated low-balance wallet, and set strict per-transaction and daily limits. <br>
Risk: An incorrect or malicious payment request could transfer funds to the wrong recipient or pay unexpected fees. <br>
Mitigation: Require explicit review of the amount, recipient address, fees, and reason before each payment. <br>
Risk: The CARDZERO_API_KEY is sensitive and can authorize wallet actions. <br>
Mitigation: Keep the API key out of ordinary chat when possible and revoke or rotate it if exposure is suspected. <br>
Risk: The artifact states the smart contract audit is in progress and recommends keeping the wallet balance below 100 USDC. <br>
Mitigation: Use low balances, owner spending rules, and conservative limits until the audit status is acceptable for the deployment. <br>


## Reference(s): <br>
- [CardZero homepage](https://cardzero.ai) <br>
- [ClawHub skill page](https://clawhub.ai/mrocker/cardzero) <br>
- [Publisher profile](https://clawhub.ai/user/mrocker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment API requests, wallet configuration values, transaction status guidance, and user-confirmation prompts.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
