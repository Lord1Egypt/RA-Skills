## Description:

Bitcoin Lightning payment CLI for agents. Lowest LSP fees. Self-custody wallet with LNURL, typed exit codes, JSON envelope output, encrypted messaging, and daemon mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovitrif](https://clawhub.ai/user/ovitrif)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to operate the Bitkit CLI for Bitcoin and Lightning wallet actions, invoices, payments, liquidity, webhooks, and encrypted messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and agent workflows can expose users to code execution risk.

Mitigation: Review and pin the installer or build from trusted source before installation.

Risk: Bitcoin and Lightning payments can cause irreversible fund loss.

Mitigation: Use small isolated wallets, set explicit fee and spending limits, and require approval before send, pay, channel, or LSP funding actions.

Risk: Wallet seed phrases can be exposed through plaintext storage, transcripts, or logs.

Mitigation: Do not use --no-password for wallets holding real funds, and keep seed phrases out of agent transcripts and logs.

## Reference(s):

- [Bitkit CLI project homepage](https://github.com/synonymdev/bitkit-cli)
- [Lightning Rapid Gossip Sync documentation](https://docs.rs/lightning-rapid-gossip-sync)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash command snippets and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use --json for parseable output; the skill requires the bitkit binary.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
