## Description:

A multi-chain wallet skill for AI agents, with local sandbox signing, secure PIN handling, and configurable risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawwalletteam](https://clawhub.ai/user/clawwalletteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use ClawWallet to install and operate a local multi-chain wallet sandbox for agent wallet setup, status checks, signing, transfers, swaps, and policy-aware wallet management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs web-delivered installer code and downloads a sandbox binary.

Mitigation: Install only after reviewing the publisher and release; prefer version-pinned releases with signed checksums before using real wallet value.

Risk: The skill uses local bearer tokens for wallet sandbox access.

Mitigation: Do not print, share, or paste AGENT_TOKEN or CLAY_AGENT_TOKEN except as an Authorization header to the local sandbox.

Risk: The artifact includes a marketplace auto-install flow.

Mitigation: Avoid marketplace auto-install for wallet use; use explicit, user-confirmed installation from a reviewed release.

Risk: Wallet transaction, reinstall, upgrade, and uninstall actions can change funds or persistent wallet state.

Mitigation: Require explicit user confirmation before transaction execution and before reinstall, upgrade, or uninstall operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawwalletteam/skills/claw-wallet-pro)
- [Project homepage](https://github.com/ClawWallet/Claw-Wallet-Skill)
- [Project repository](https://github.com/ClawWallet/Claw-Wallet-Skill)
- [Binary repository](https://github.com/ClawWallet/Claw_Wallet_Bin)
- [Distribution host](https://www.clawwallet.cc/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API calls, wallet status summaries, and confirmation prompts before transaction or lifecycle actions.]

## Skill Version(s):

0.1.4 (source: server release metadata and skill.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
