## Description:

Play Colony game on Solana — buy lands, upgrade, claim $OLO earnings, swap tokens via Jupiter. Full autonomous gameplay with strategy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manylov](https://clawhub.ai/user/manylov)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to run an OpenClaw agent that manages a Colony game wallet on Solana, including land purchases, upgrades, claims, Jupiter swaps, and ROI-based recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously spend real crypto through land purchases, upgrades, and token swaps.

Mitigation: Install only with a dedicated low-balance Solana wallet and require an external approval process before unattended swaps or spending.

Risk: Generated private-key output and the SOLANA_PRIVATE_KEY environment variable are sensitive signing material.

Mitigation: Treat generated private keys as secrets, avoid sharing them, and keep funded wallets separate from other assets.

Risk: Solana transactions and token burns are generally irreversible once confirmed.

Mitigation: Use swap quotes, price checks, transaction status checks, and conservative funding before executing write commands.

Risk: The Colony program authority model and game state can affect wallet funds and claim behavior.

Mitigation: Review the Colony program authority model and current game state before funding or operating the wallet.

## Reference(s):

- [Colony game](https://colony.game)
- [Jupiter Portal](https://portal.jup.ag)
- [ClawHub skill page](https://clawhub.ai/manylov/skills/colony-solana)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require a Solana private key, RPC access, and a Jupiter API key for swaps, price checks, or quotes.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
