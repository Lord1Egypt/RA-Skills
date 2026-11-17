## Description:

Connect to EmblemVault and manage crypto wallets via Emblem AI - Agent Hustle. Supports Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genecyber](https://clawhub.ai/user/genecyber)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent connect to EmblemVault and Agent Hustle for wallet addresses, balances, portfolio queries, swaps, transfers, and other crypto actions across supported chains. It is intended for workflows where users can supply wallet credentials and review transaction approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required global npm CLI can receive wallet-level authority.

Mitigation: Verify or pin the package before installing and start with a low-value or test wallet.

Risk: Wallet passwords, local credentials, and session files can grant access to funds if exposed.

Mitigation: Prefer browser authentication, avoid putting passwords in command-line arguments, shell history, scripts, or environment variables, and protect `~/.emblemai/`.

Risk: Wallet-modifying actions such as swaps, transfers, or signing can move funds.

Mitigation: Review every transaction detail before approving any wallet-modifying action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/genecyber/skills/emblemai-agentwallet)
- [Publisher Profile](https://clawhub.ai/user/genecyber)
- [EmblemVault](https://emblemvault.dev)
- [Agent Wallet npm Package](https://www.npmjs.com/package/@emblemvault/agentwallet)
- [Agent Hustle](https://agenthustle.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a local CLI, wallet credential setup, and user confirmation before wallet-modifying actions.]

## Skill Version(s):

3.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
