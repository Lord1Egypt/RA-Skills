## Description:

CDP Wallet lets an agent read balances, send USDC on Base, inspect transfer history, and pay x402-protected resources through a Coinbase CDP server wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ales375](https://clawhub.ai/user/ales375)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs a persistent Coinbase CDP server wallet for USDC payments, balance checks, transfer review, or x402 settlements on Base without handling private keys directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can spend real funds through send-usdc or pay-x402 without built-in transaction limits, allowlists, or confirmation gates.

Mitigation: Use a dedicated low-balance wallet, configure CDP policy limits, and require operator approval or allowlists before payment commands.

Risk: CDP credentials and the wallet secret can authorize signing if exposed to an untrusted agent, workspace, or tenant.

Mitigation: Restrict environment variable access to approved agents and treat CDP_WALLET_SECRET like a private key.

Risk: pay-x402 can pay arbitrary URLs and may forward authorization headers to untrusted services.

Mitigation: Limit allowed x402 endpoints and prevent agents from sending authorization headers to untrusted URLs.

## Reference(s):

- [ClawHub CDP Wallet Skill](https://clawhub.ai/ales375/skills/cdp-wallet)
- [Publisher Profile](https://clawhub.ai/user/ales375)
- [Project Homepage](https://github.com/Ales375/openclaw-cdp-wallet-skill)
- [Coinbase CDP Server Wallets v2 Documentation](https://docs.cdp.coinbase.com/server-wallets/v2/introduction/welcome)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands emit single-line JSON with ok/error status, wallet addresses, balances, transaction hashes, and x402 settlement details.]

## Skill Version(s):

0.2.2 (source: SKILL.md frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
