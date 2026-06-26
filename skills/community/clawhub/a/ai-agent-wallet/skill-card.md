## Description: <br>
Agent-Wallet provides local Node.js wallet workflows for creating or importing wallets, checking balances, signing messages, and sending native or ERC-20 transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beardkoda](https://clawhub.ai/user/beardkoda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and wallet operators use this skill to run local wallet generation or import, balance checks, message signing, and confirmed transfer flows from agent-guided Node.js scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages local wallet files and signing authority, so misuse or compromised files can expose funds. <br>
Mitigation: Use a new low-value wallet, keep WALLET_SECRET_KEY strong and private, protect wallet/signer.json from backup or sync exposure, and review every signature or transaction before running scripts. <br>
Risk: Transaction broadcasts can transfer native or ERC-20 assets on the configured network. <br>
Mitigation: Verify the chain, recipient, amount, and token contract before use; require --confirm=true for broadcasts and --confirmMainnet=true for supported mainnet chain IDs. <br>
Risk: Import flows may involve seed phrases or private keys supplied to command-line scripts. <br>
Mitigation: Avoid importing a primary wallet or high-value secret, prefer generated low-value wallets, and do not expose seed phrases or private keys in chat, logs, shell history, or shared terminals. <br>


## Reference(s): <br>
- [Agent-Wallet ClawHub release page](https://clawhub.ai/beardkoda/ai-agent-wallet) <br>
- [Agent-Wallet changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet scripts use local wallet files, require WALLET_SECRET_KEY for encrypted signer material, and require explicit confirmation before transaction broadcast.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter, changelog released 2026-04-14, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
