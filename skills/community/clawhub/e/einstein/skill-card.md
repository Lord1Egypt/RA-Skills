## Description:

Blockchain analytics and DeFi intelligence via Einstein's x402 micropayment services for on-chain market analysis, token research, whale tracking, smart money tracking, rug pull scanning, launchpad monitoring, portfolio analysis, MEV detection, cross-chain arbitrage, and Polymarket data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuxo](https://clawhub.ai/user/chuxo)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to run paid and free blockchain intelligence queries across supported chains, including market movement, token risk, wallet, launchpad, MEV, arbitrage, NFT, and prediction-market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet payments and private keys, and the authoritative security verdict requires careful human review before installation.

Mitigation: Review before installing, use only a dedicated low-balance wallet, and prefer EINSTEIN_X402_PRIVATE_KEY over saved config files.

Risk: A configured endpoint controls the payment challenge that the wallet signs.

Mitigation: Use only a trusted endpoint, keep payment confirmation enabled, verify the displayed cost for each paid query, and avoid autoConfirm for routine use.

Risk: Command-line private-key entry and saved config can expose wallet credentials through local process, shell, or file handling.

Mitigation: Avoid --key and --save-config unless necessary; if config.json is used, restrict file permissions and keep it out of version control.

## Reference(s):

- [Einstein homepage](https://emc2ai.io)
- [ClawHub skill page](https://clawhub.ai/chuxo/skills/einstein)
- [Einstein x402 Services Catalog](artifact/references/services-catalog.md)
- [Einstein x402 Payment Guide](artifact/references/payment-guide.md)
- [Einstein x402 Usage Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid queries can return raw structured data or AI-analyzed blockchain intelligence; free service commands may return JSON search results.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
