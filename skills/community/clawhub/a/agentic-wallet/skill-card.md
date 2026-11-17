## Description:

Create and manage crypto wallets for AI agents across Coinbase, Tempo/Stripe, MoonPay/OpenWallet, and Crossmint with non-interactive setup, JSON output, backup and recovery, and multi-chain support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smukh](https://clawhub.ai/user/smukh)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers and agent builders use this skill to let agents create wallets, check balances, receive or send payments, and prepare wallets for x402 or Machine Payments Protocol workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned npm wallet tool that can interact with secrets and funds.

Mitigation: Use a pinned, reviewed package version in an isolated environment before allowing access to funded wallets or production credentials.

Risk: Password files, API keys, seed phrases, and wallet backups can provide full wallet control if exposed.

Mitigation: Store secrets in protected files or secret managers, restrict filesystem permissions, avoid placing real secrets directly in shell commands, and rotate any exposed credentials.

Risk: Funding instructions or wallet addresses may lead to irreversible transfers if copied incorrectly or produced by an untrusted package.

Mitigation: Independently verify recipient and funding addresses, test with low-value transfers first, and require human approval for material fund movement.

## Reference(s):

- [Agentic Wallet ClawHub page](https://clawhub.ai/smukh/skills/agentic-wallet)
- [agentic-wallet npm package](https://www.npmjs.com/package/agentic-wallet)
- [Agentic Wallet project page](https://github.com/smukh/agentic-wallet)
- [Coinbase Agentic Wallet documentation](https://docs.cdp.coinbase.com/agentic-wallet/welcome)
- [Tempo documentation](https://docs.tempo.xyz/)
- [OpenWallet documentation](https://docs.openwallet.sh/)
- [Crossmint platform documentation](https://docs.crossmint.com/introduction/platform-overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to run npx agentic-wallet commands and may produce provider-specific JSON responses from the underlying CLI.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
