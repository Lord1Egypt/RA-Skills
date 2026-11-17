## Description:

Openclaw Fomo3d provides a CLI for playing Fomo3D and Slot Machine on BNB Chain, including status checks, share purchases, dividend claims, token trading, slot spins, and wallet actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erenvance](https://clawhub.ai/user/erenvance)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to interact with Fomo3D and slot-machine game contracts on BNB Chain through agent-run CLI commands. It supports wallet checks, game status queries, share purchases, exits, settlements, token trades, slot spins, deposits, and claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill signs real BNB Chain transactions and may handle a wallet private key, including setup flows that can write the key to local configuration.

Mitigation: Use a fresh wallet funded only with amounts you are willing to lose, avoid valuable private keys, prefer environment-based secret handling, and review the network and transaction before execution.

Risk: The CLI can grant broad ERC20 token approvals to game and trading contracts.

Mitigation: Review spender addresses and approval transactions before signing, keep only limited funds in the wallet, and revoke token allowances after use.

Risk: Game, slot, deposit, buy, and sell actions can lose funds or permanently lock deposited tokens.

Mitigation: Start on testnet or with small amounts, verify command parameters carefully, and review every buy, sell, bet, deposit, and claim before execution.

## Reference(s):

- [Fomo3D Homepage](https://fomo3d.app)
- [ClawHub Skill Page](https://clawhub.ai/erenvance/skills/fomo3d)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses wei-denominated token amounts and can emit machine-readable JSON when commands are run with --json.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
