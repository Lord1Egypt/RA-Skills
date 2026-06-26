## Description: <br>
Trust scoring for AI agents. Log transactions and submit payment proofs to build a verifiable BOB Score, a trust score that other agents and services can check before doing business with yours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bankofbotsandy](https://clawhub.ai/user/bankofbotsandy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect AI agents to Bank of Bots financial workflows, check balances and policies, record transactions, initiate payments, submit payment proofs, and inspect trust score history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad payment, banking, webhook, API-key, budget, sub-agent, and key-rotation authority. <br>
Mitigation: Install only when Bank of Bots financial workflows are intended, use least-privilege keys stored outside chat and logs, and require human approval before sends, payouts, counterparty changes, webhooks, budget changes, sub-agent creation, or key rotation. <br>
Risk: Sensitive bank details, API keys, and event payloads may be exposed through commands, logs, or untrusted webhook targets. <br>
Mitigation: Keep credentials out of prompts and logs, verify webhook destinations, and avoid sending bank details or event payloads to untrusted systems. <br>
Risk: Payment actions can fail or be denied by policies, kill switches, rate limits, insufficient funds, or proof requirements. <br>
Mitigation: Check ok before using response data, follow next_actions for recovery, stop transaction attempts on kill-switch denials, and do not retry denied transactions without changing the parameters. <br>


## Reference(s): <br>
- [Bank of Bots agent setup guide](https://app.bankofbots.ai/docs/agent-setup) <br>
- [Bank of Bots API endpoint](https://api.bankofbots.ai/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/bankofbotsandy/bank-of-bots) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bankofbotsandy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return structured JSON with ok, data, and next_actions fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
