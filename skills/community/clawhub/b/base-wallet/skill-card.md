## Description:

Base Wallet helps agents create Base/Ethereum wallets, sign SIWE messages, check balances, send transactions, and register for BaseMail without browser extensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give autonomous agents a Base-compatible crypto identity for wallet creation, wallet inspection, transaction signing, and BaseMail registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys and signatures.

Mitigation: Use a new low-value wallet, protect the host and backups, and review each BaseMail signing action before approving use.

Risk: Managed wallet mode can persist private keys and mnemonics on disk.

Mitigation: Prefer environment-variable mode; use managed mode only when the host and backups are protected and wallet files are excluded from source control.

Risk: Server security guidance flags unresolved SIWE validation and wallet-name path validation concerns.

Mitigation: Do not reuse a valuable wallet with this skill until those issues are fixed and reviewed.

## Reference(s):

- [BaseMail API Reference](references/basemail-api.md)
- [BaseMail API](https://api.basemail.ai)
- [Base Mainnet RPC](https://mainnet.base.org)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript and bash examples plus command-line script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet addresses, private keys, mnemonics, SIWE signatures, transaction hashes, balance information, audit log entries, and optional managed wallet files.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
