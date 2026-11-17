## Description:

AAWP (AI Agent Wallet Protocol) is a wallet skill for AI agents on EVM-compatible blockchains that supports wallet lifecycle management, token transfers, DEX swaps, cross-chain bridging, contract interactions, DCA automation, and price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wfce](https://clawhub.ai/user/wfce)

### License/Terms of Use:

BUSL-1.1

## Use Case:

External developers and AI-agent operators use this skill to provision and operate AI-controlled wallets across EVM chains. It can guide wallet setup and produce commands for transfers, swaps, bridging, contract reads and writes, scheduled DCA, price alerts, portfolio checks, NFT operations, and DeFi workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and runtime setup are powerful and mutable because runtime files and a native signing component are fetched during provisioning.

Mitigation: Review before install, audit and pin the remote runtime, and verify every downloaded file before execution.

Risk: The skill can submit on-chain transactions, register scheduled jobs, and operate with wallet signing authority.

Mitigation: Use a low-value wallet in an isolated environment first, set strict limits for automated trading and contract calls, and require human approval for provisioning, wallet creation, cron registration, and binary approval.

Risk: The signing daemon manages sensitive key material and relies on a native binary.

Mitigation: Install only into the intended client, verify binary approval and provenance before use, and keep guardian and wallet configuration pinned to avoid operating the wrong wallet.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wfce/skills/aawp)
- [AAWP documentation](https://aawp.ai)
- [Runtime repository referenced by artifact metadata](https://github.com/aawp-ai/aawp)
- [AAWP factory contract on Base](https://basescan.org/address/0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference wallet addresses, chain names, cron schedules, and transaction parameters supplied by the user or local configuration.]

## Skill Version(s):

1.6.8 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
