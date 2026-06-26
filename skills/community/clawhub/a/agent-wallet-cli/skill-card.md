## Description: <br>
Agent Wallet CLI helps agents manage self-custodial crypto wallets across Ethereum, Solana, Polygon, Arbitrum, and Base for balances, transfers, signing, approvals, history, x402 payments, and wallet lifecycle tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donald-jackson](https://clawhub.ai/user/donald-jackson) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can enable agents to inspect wallet state and perform wallet operations through agent-wallet-cli, including balance checks, transfers, token approvals, signing, history, and x402 payments. It is suited to carefully controlled automation around dedicated crypto wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can move real crypto funds, sign messages, create approvals, export wallets, or initiate x402 payments when given sufficient wallet authority. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit approval for sends, approvals, signatures, exports, and payments, run dry-runs where possible, and set strict x402 maximum amounts. <br>
Risk: Wallet passwords, mnemonics, and session tokens are sensitive credentials that can expose funds if logged or shared. <br>
Mitigation: Unlock the wallet yourself when possible, provide only short-lived session tokens, avoid giving agents WALLET_PASSWORD, and never log or share tokens or mnemonics. <br>
Risk: x402 payment behavior involves outbound HTTP requests and automatic payment retries. <br>
Mitigation: Restrict use to trusted URLs, set maximum payment amounts, require approval before payment, and review outbound request details. <br>
Risk: The npm package supply chain can affect wallet safety when real funds are used. <br>
Mitigation: Audit or pin the npm package and verify it against the declared source repository before using real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donald-jackson/agent-wallet-cli) <br>
- [agent-wallet-cli repository declared in skill metadata](https://github.com/donald-jackson/agent-wallet-cli) <br>
- [agent-wallet-cli npm package](https://www.npmjs.com/package/agent-wallet-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI operations can return JSON or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent-wallet-cli binary; may use sensitive WALLET_PASSWORD and WALLET_SESSION_TOKEN environment values] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
