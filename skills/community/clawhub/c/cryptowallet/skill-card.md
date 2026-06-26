## Description: <br>
CryptoWallet helps agents create and import EVM and Solana wallets, check native and token balances, send transactions, and interact with smart contracts using encrypted local key storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnufoo](https://clawhub.ai/user/gnufoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, Web3 operators, and external users use this skill to manage local blockchain wallets, inspect balances, send native or token transfers, and perform smart-contract reads or writes across supported EVM and Solana networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast irreversible blockchain transactions. <br>
Mitigation: Use testnets or small amounts first and independently verify every address, amount, network, token contract, and smart-contract call before execution. <br>
Risk: Wallet secrets and passwords may be handled through command-line arguments. <br>
Mitigation: Avoid passing real private keys or wallet passwords directly on the command line, and prefer isolated test wallets before using production funds. <br>
Risk: Public or untrusted RPC endpoints can affect reliability and transaction visibility. <br>
Mitigation: Configure trusted RPC endpoints where possible and verify network settings before balance checks, transfers, or contract writes. <br>


## Reference(s): <br>
- [Network Configuration](artifact/references/networks.json) <br>
- [Security Best Practices](artifact/references/security.md) <br>
- [ClawHub Release Page](https://clawhub.ai/gnufoo/cryptowallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create encrypted wallet files, query public RPC endpoints, and submit signed blockchain transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
