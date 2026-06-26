## Description: <br>
ClawLaunch helps agents launch and trade AI agent tokens on a Base bonding curve, including token creation, token discovery, price quotes, buy and sell flows, on-chain memos, and Base Mainnet/Base Sepolia support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SmokeAlot420](https://clawhub.ai/user/SmokeAlot420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use this skill to configure ClawLaunch API access, launch AI agent tokens, list tokens, check prices, retrieve memos, and prepare buy or sell transaction calldata for Base bonding-curve trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real token launches and trading actions. <br>
Mitigation: Use Base Sepolia or a low-balance isolated wallet first, require manual confirmation before launches or signed transactions, and set explicit spend and sell limits. <br>
Risk: The API key grants access to launch and trade operations. <br>
Mitigation: Store the key privately, use least-privilege access, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: Transaction calldata and chain settings may direct funds or actions to unintended targets if not reviewed. <br>
Mitigation: Verify the chain ID, destination address, calldata, value, slippage, and token address before broadcasting any transaction. <br>
Risk: Trade memos are intended to be recorded on-chain and can be permanent public data. <br>
Mitigation: Do not include secrets, private information, or sensitive business context in memos. <br>


## Reference(s): <br>
- [ClawLaunch Skill Page](https://clawhub.ai/SmokeAlot420/clawlaunch) <br>
- [ClawLaunch Homepage](https://www.clawlaunch.fun) <br>
- [ClawLaunch API Documentation](references/api-docs.md) <br>
- [ClawLaunch Token Trading Reference](references/token-trading.md) <br>
- [ClawLaunch Agent Autonomy Patterns](references/agent-patterns.md) <br>
- [ClawLaunch Error Handling Reference](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, API request payloads, code snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, a ClawLaunch API key, and a wallet able to sign Base transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
