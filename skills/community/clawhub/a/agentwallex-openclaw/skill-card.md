## Description: <br>
Create and manage AI agents, send USDC/USDT payments, check balances across Ethereum, BSC, and Tron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HexCupe](https://clawhub.ai/user/HexCupe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure AgentWallex credentials, manage AI-agent wallets, check balances, and send or track USDC/USDT payments across supported Ethereum, BSC, and Tron networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real USDC or USDT funds to arbitrary recipient addresses when production credentials and a production API endpoint are used. <br>
Mitigation: Use sandbox or testnet first, require manual review of recipient address, chain, token, amount, and environment before every transfer, and keep human confirmation enabled for transfer and pay actions. <br>
Risk: Payment-capable AgentWallex API credentials are stored in a local configuration file. <br>
Mitigation: Protect ~/.openclaw/agentwallex/config.json, use limited and revocable API keys, avoid sharing the host account, and remove the local config when access is no longer needed. <br>
Risk: Choosing the wrong chain, token, recipient address format, or environment can cause failed transactions or unintended live payments. <br>
Mitigation: Validate address format for the selected chain, confirm token support, check available balance before sending, and explicitly distinguish sandbox from production before executing payment workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HexCupe/agentwallex-openclaw) <br>
- [AgentWallex Homepage](https://agentwallex.com) <br>
- [AgentWallex Docs](https://docs.agentwallex.com) <br>
- [AgentWallex Dashboard](https://app.agentwallex.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, API request examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, stores credentials at ~/.openclaw/agentwallex/config.json, and requires human confirmation for transfer and pay actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
