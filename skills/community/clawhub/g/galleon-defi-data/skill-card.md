## Description:

Connects CoinGecko, DefiLlama and AIXBT data sources to assess DeFi prices, protocol metrics, narratives and yield with source identity and freshness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi researchers use this skill to configure data access and compare market, protocol and yield evidence while checking asset identity, timestamps, source coverage and material limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid data access or API calls can consume account credits and expose credentials.

Mitigation: Keep enrollment and credentials user-controlled; limit reads to the requested task and do not log secrets.

Risk: Wallet and portfolio lookups can reveal sensitive financial context.

Mitigation: Use only needed addresses and avoid including private account identifiers in shared outputs.

Risk: Stale or mismatched market data can be mistaken for an executable quote or verified position.

Mitigation: Check asset and chain identity, timestamps and source coverage; verify consequential facts against current protocol or chain evidence.

## Reference(s):

- [Galleon DeFi Data release](https://clawhub.ai/galleonlabs/skills/galleon-defi-data)
- [Provider access and setup](artifact/references/providers.md)
- [Data interpretation and provenance](artifact/references/methodology.md)
- [Public price diagnostic](artifact/references/diagnostic.md)
- [Product diligence](artifact/references/diligence.md)

## Skill Output:

**Output Type(s):** [Analysis, Configuration instructions, Shell commands, JSON]

**Output Format:** [Markdown guidance and optional JSON price diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dated source identity, access gaps and material limitations; does not authorize trades.]

## Skill Version(s):

0.6.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
