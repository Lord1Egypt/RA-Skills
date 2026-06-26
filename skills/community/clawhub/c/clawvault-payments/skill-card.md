## Description: <br>
Security middleware for AI agents handling money, covering non-custodial crypto wallets and virtual Visa cards with spending limits, whitelists, and human approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewszk1](https://clawhub.ai/user/andrewszk1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent request ClawVault crypto payments or Agent Card purchases while checking rules, surfacing approval states, and avoiding logging card credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can interact with ClawVault for real crypto payments or card purchases. <br>
Mitigation: Configure strict spending limits, recipient or merchant allowlists, and approval rules before use. <br>
Risk: Card credentials and API keys are sensitive and could be exposed through logs or storage. <br>
Mitigation: Never log or store card credentials or API keys; use temporary card credentials immediately. <br>
Risk: Transactions may require approval, be denied, or expire before execution. <br>
Mitigation: Check transaction status and clearly tell the user when approval is required in Telegram or the ClawVault dashboard. <br>


## Reference(s): <br>
- [ClawVault Documentation](https://clawvault.cc/docs) <br>
- [ClawVault Agent API Key Setup](https://clawvault.cc/agents) <br>
- [ClawVault API Base URL](https://api.clawvault.cc) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWVAULT_API_KEY; payment and card actions may require human approval and must avoid logging card credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
