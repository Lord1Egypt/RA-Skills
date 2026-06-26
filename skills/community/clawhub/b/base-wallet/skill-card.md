## Description: <br>
Base Wallet creates and manages Base/Ethereum wallets for AI agents, including SIWE message signing, balance checks, transaction examples, and BaseMail registration flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create Base-compatible wallets, load wallet credentials, sign SIWE messages, check balances, and register a wallet-backed BaseMail identity. It is intended for agents that need programmatic Web3 identity or wallet-linked service access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and use crypto wallets, handle private keys, and sign SIWE messages. <br>
Mitigation: Use a test or low-value wallet first, keep private keys out of shared shells and CI logs, and require explicit human approval before signing, registration, purchases, or blockchain transactions. <br>
Risk: Managed wallet mode writes wallet and mnemonic files under the user's home directory. <br>
Mitigation: Prefer environment-variable mode, inspect any generated wallet and mnemonic files, restrict access to the files, back up mnemonics offline, and delete unnecessary mnemonic backups. <br>
Risk: BaseMail registration and related flows can contact external services and may involve wallet-linked identity, email actions, or credits. <br>
Mitigation: Review the requested action and destination service before execution, and require explicit approval for BaseMail registration, email activity, credit purchases, or transactions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daaab/base-wallet) <br>
- [BaseMail API Reference](references/basemail-api.md) <br>
- [BaseMail API](https://api.basemail.ai) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [Base Sepolia RPC](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and JavaScript examples; scripts may emit environment variable exports, JSON wallet data, audit log entries, and BaseMail registration output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read wallet files under the user's home directory and may contact Base, Basescan, and BaseMail endpoints when executed.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
