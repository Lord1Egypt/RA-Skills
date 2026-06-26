## Description: <br>
Create and manage crypto wallets for AI agents across Coinbase, Tempo/Stripe, MoonPay/OpenWallet, and Crossmint with non-interactive mode, JSON output, backup/recovery, and multi-chain support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smukh](https://clawhub.ai/user/smukh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create, inspect, fund, back up, and recover agent wallets for payments, x402-gated APIs, Machine Payments Protocol workflows, and blockchain protocol interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet secrets, API keys, passwords, and seed phrases can authorize access to funds if exposed in chat, shell history, logs, or shared files. <br>
Mitigation: Use secret files with restrictive permissions or a secret manager, avoid echoing real secrets, and never paste seed phrases, private keys, API keys, or wallet passwords into chat or logs. <br>
Risk: Agent wallets may initiate payments or transactions with real financial impact. <br>
Mitigation: Keep only limited funds in agent wallets and review any payment or transaction before authorizing it. <br>
Risk: The skill relies on the agentic-wallet npm package and wallet providers for wallet operations. <br>
Mitigation: Install only when the npm package and the selected wallet providers are trusted for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smukh/agentic-wallet) <br>
- [npm package](https://www.npmjs.com/package/agentic-wallet) <br>
- [Coinbase Agentic Wallet documentation](https://docs.cdp.coinbase.com/agentic-wallet/welcome) <br>
- [Tempo documentation](https://docs.tempo.xyz/) <br>
- [OpenWallet documentation](https://docs.openwallet.sh/) <br>
- [Crossmint documentation](https://docs.crossmint.com/introduction/platform-overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can request JSON output for programmatic agent workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
