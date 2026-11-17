## Description:

Base Wallet helps AI agents create and manage Base/Ethereum-compatible wallets, sign SIWE messages, check balances, and send transactions without browser extensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pin-alt](https://clawhub.ai/user/pin-alt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to give AI agents command-line wallet operations on Base/Ethereum, including wallet creation, SIWE signing, balance checks, transactions, and BaseMail registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private keys, mnemonics, wallet files, .env entries, stdout, and audit logs can expose wallet control material.

Mitigation: Use test wallets first, avoid funded wallets until review is complete, prefer secret-manager or environment-variable storage, restrict file permissions, and treat all wallet-related outputs and logs as sensitive.

Risk: Signing, transaction, and BaseMail registration workflows can create durable blockchain or account-linking effects.

Mitigation: Review every message, endpoint, recipient, chain, and transaction value before execution; run only intended registrations or transactions and start on test networks when possible.

Risk: Managed wallet mode writes private keys and mnemonic backups to local files.

Mitigation: Prefer environment-variable mode, inspect the configured wallet directory before use, keep managed files out of source control, and remove offline backup material from connected systems after secure backup.

## Reference(s):

- [BaseMail API Reference](references/basemail-api.md)
- [ClawHub Skill Page](https://clawhub.ai/pin-alt/skills/2026-02-10-clawhub-base-wallet-1-5-0)
- [Base Mainnet RPC Endpoint](https://mainnet.base.org)
- [Base Sepolia RPC Endpoint](https://sepolia.base.org)
- [BaseMail Service](https://basemail.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and JavaScript examples; bundled scripts may emit shell exports, JSON, balances, transaction hashes, and registration status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles wallet secrets and network calls; generated keys, mnemonics, wallet files, .env files, and audit logs should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json lists 1.1.0 and artifact/_meta.json lists 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
