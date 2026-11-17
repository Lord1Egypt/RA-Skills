## Description:

Bitcoin L1 wallet for agents - check balances, send BTC, manage UTXOs. Extends to Stacks L2 (STX, DeFi) and Pillar smart wallets (sBTC yield).

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoabuddy](https://clawhub.ai/user/whoabuddy)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent inspect Bitcoin balances and fees, manage encrypted wallets, send BTC, and optionally operate Stacks L2, Pillar smart wallet, inscriptions, x402 paid API, and identity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad wallet actions, including fund movement, signing, DeFi actions, inscriptions, paid API calls, and identity workflows.

Mitigation: Start on testnet or with a low-value wallet and require explicit approval before transfers, contract calls, DeFi actions, inscriptions, paid API calls, or identity registration.

Risk: Install examples use an unpinned package selector, which can change what code is installed over time.

Mitigation: Use a pinned and verified MCP package version instead of @latest.

Risk: Headless wallet automation and auto-unlock behavior can expose valuable funds to unintended agent actions.

Mitigation: Avoid headless auto-unlock with valuable funds, lock wallets after use, and keep separate operational wallets for automation.

Risk: Public identity and social-claim workflows can link wallet addresses to public profiles or agent reputation activity.

Mitigation: Use separate addresses for public identity or social-claim workflows when privacy or account separation matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoabuddy/skills/aibtc-bitcoin-wallet)
- [npm package](https://www.npmjs.com/package/@aibtc/mcp-server)
- [GitHub repository metadata link](https://github.com/aibtcdev/aibtc-mcp-server)
- [Stacks L2 DeFi](references/stacks-defi.md)
- [Pillar Smart Wallet](references/pillar-wallet.md)
- [Bitcoin Inscription Workflow](references/inscription-workflow.md)
- [x402 Inbox Flow](references/x402-inbox.md)
- [Genesis Agent Lifecycle](references/genesis-lifecycle.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and wallet workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide agent requests for wallet operations, signing, fund movement, paid API calls, and identity workflows.]

## Skill Version(s):

1.26.0 (source: ClawHub release evidence; artifact metadata reports 1.14.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
