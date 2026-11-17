## Description:

Gekko is an AI-powered DeFi portfolio manager for the Base network that analyzes yield opportunities, portfolio allocations, and market intelligence using Morpho, Yearn, and DexScreener data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekkoai001](https://clawhub.ai/user/gekkoai001)

### License/Terms of Use:


## Use Case:

External users and developers use Gekko to query a remote DeFi agent for Base-network yield analysis, portfolio allocation recommendations, token analysis, and market intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can return financial guidance about DeFi yields, vaults, or trades that may be incorrect, stale, or unsuitable for a user's risk profile.

Mitigation: Treat responses as informational and independently verify APY, vault, and trading recommendations before moving funds.

Risk: The skill sends requests to a third-party API endpoint.

Mitigation: Avoid sharing private keys, seed phrases, or unnecessary wallet and account details in requests.

## Reference(s):

- [Gekko ClawHub skill page](https://clawhub.ai/gekkoai001/skills/gekko)
- [Gekko A2A API endpoint](https://gekkoterminal.ai/api/a2a?agent=gekko)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with JSON API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API responses may include APY, TVL, risk profile, token price, volume, liquidity, trend, and allocation recommendations.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
