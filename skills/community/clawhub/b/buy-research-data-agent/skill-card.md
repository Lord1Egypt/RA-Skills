## Description: <br>
Agent purchases paid datasets, API credits, or research reports using CAI wallet after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and agent operators use this skill to identify paid datasets, API credits, or research reports, prepare CAI wallet funding, and execute a transfer only after confirming recipient and amount. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet transfers may be irreversible or sent to an incorrect recipient, asset, or network. <br>
Mitigation: Before approving any transfer, verify the recipient, amount, asset or network, and refund terms; prefer a limited-balance wallet when available. <br>
Risk: The skill requires a sensitive CAI API key for paid wallet and payment actions. <br>
Mitigation: Store the key with the agent secret manager and prefer a scoped or limited API key when available. <br>
Risk: The agent may not discover every paywall or checkout detail on its own. <br>
Mitigation: Require the agent to surface the product, price, payment method, and payee details before the user confirms payment. <br>


## Reference(s): <br>
- [CAI Skill Reference](https://cai.com/skill.md) <br>
- [CAI Agent Payment](https://cai.com/agent-payment.html) <br>
- [CAI Developers](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and wallet action steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY and explicit user confirmation before transfer.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
