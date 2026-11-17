## Description:

Automated crypto airdrop discovery and daily market analysis that finds high-funding projects, tracks market structure, support and resistance, and macro news without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ismaonezain](https://clawhub.ai/user/ismaonezain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and crypto traders use this skill to generate airdrop opportunity drafts, daily market summaries, and periodic alert text for manual review. It is intended to support research workflows, not to replace current market verification or financial judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated crypto reports may overstate live discovery or present hardcoded or mock guidance as current information.

Mitigation: Treat reports as informational drafts and verify projects, funding, token status, links, and market conditions against current independent sources before acting.

Risk: Airdrop quests, bridges, testnets, and linked project activity can expose users to wallet, phishing, or transaction risk.

Mitigation: Use wallet-safety practices, review URLs manually, avoid valuable wallets for experiments, and understand each transaction before signing.

Risk: Trading guidance may be incomplete or stale because the security evidence warns that the skill is not a reliable live airdrop-discovery system.

Mitigation: Do not rely on generated trading guidance without separate current market research and human review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ismaonezain/skills/crypto-airdrop-hunter)
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, console text, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated reports under reports/ and updates state.json during heartbeat checks.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
