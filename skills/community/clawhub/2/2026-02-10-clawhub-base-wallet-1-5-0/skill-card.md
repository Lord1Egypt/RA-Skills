## Description: <br>
Base Wallet creates and manages Base/Ethereum-compatible wallets for agents, including SIWE message signing, balance checks, and transaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pin-alt](https://clawhub.ai/user/pin-alt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to create low-level wallet identity, sign SIWE authentication messages, check Base-chain balances, and initiate wallet-backed workflows for autonomous agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or persist raw wallet private keys or mnemonics during wallet setup. <br>
Mitigation: Use a fresh low-value wallet, prefer an external secret manager or tightly scoped environment variables, and avoid storing secrets in shell history, shared .env files, or committed files. <br>
Risk: The skill can sign SIWE messages and register remote BaseMail accounts with an agent-accessible wallet. <br>
Mitigation: Review the registration and signing flow before execution, confirm the remote service and message contents, and avoid funding the wallet beyond the amount you are prepared to lose. <br>


## Reference(s): <br>
- [BaseMail API Reference](references/basemail-api.md) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [Base Sepolia RPC](https://sepolia.base.org) <br>
- [BaseMail API](https://api.basemail.ai) <br>
- [Skill Release Page](https://clawhub.ai/pin-alt/2026-02-10-clawhub-base-wallet-1-5-0) <br>
- [Publisher Profile](https://clawhub.ai/user/pin-alt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI-oriented wallet setup guidance and commands; generated wallet material may include private keys or mnemonics that require secure handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.5.0, while package.json and the artifact changelog report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
