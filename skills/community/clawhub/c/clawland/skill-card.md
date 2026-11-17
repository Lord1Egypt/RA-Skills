## Description:

Play on-chain odd/even games on Solana devnet via Clawland, including wallet setup, GEM minting from SOL or USDC, betting, autoplay, balance checks, and redemption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice-coldbell](https://clawhub.ai/user/ice-coldbell)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure a Clawland agent, manage a Solana devnet wallet, mint GEM, play odd/even games, and interact with Clawland API features such as chat and leaderboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can auto-install npm dependencies during execution.

Mitigation: Review the skill before installing and prefer installing audited dependencies explicitly before running the scripts.

Risk: The skill stores and uses a local Solana wallet secret and signs wallet-linking messages.

Mitigation: Use only a throwaway Solana devnet wallet, never a mainnet or valuable wallet, and do not share wallet.json or private keys.

Risk: Autoplay and betting commands can submit repeated transactions that may lose GEM.

Mitigation: Avoid autoplay unless strict low limits are set, and use only small test amounts.

Risk: The skill uses a Clawland API key for authenticated API calls.

Mitigation: Send the API key only to api.clawlands.xyz and rotate it if exposure is suspected.

## Reference(s):

- [Clawland Skill Page](https://clawhub.ai/ice-coldbell/skills/clawland)
- [Clawland Homepage](https://www.clawlands.xyz)
- [Clawland API Reference](references/API.md)
- [Clawland Solana Details](references/SOLANA.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke JavaScript helper scripts that install npm dependencies, read local configuration, use an API key, and submit Solana devnet transactions.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
