## Description: <br>
The agent's wallet. Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to create an agent-controlled EVM wallet, check balances, transfer tokens, swap assets, and submit smart contract transactions within owner-defined policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can move funds, perform swaps, and call arbitrary smart contracts if wallet policies are unset or too permissive. <br>
Mitigation: Use testnets or very small balances first, claim the wallet immediately, set strict address, token, function, and spending policies, and require human approval for sensitive transactions. <br>
Risk: The wallet API key functions like a financial credential for future wallet actions. <br>
Mitigation: Store the API key securely, avoid exposing it in prompts or logs, and rotate or revoke access if it may have been shared. <br>


## Reference(s): <br>
- [ClawHub Agent Wallet listing](https://clawhub.ai/glitch003/agent-wallet) <br>
- [SafeSkill service endpoint](https://safeskill-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Bearer API key returned at wallet creation and may return wallet addresses, balances, claim URLs, transaction status, or approval-pending status.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
