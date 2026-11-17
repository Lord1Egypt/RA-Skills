## Description:

Compare all Uniswap pools for a token pair across fee tiers and versions. Use when the user asks which pool is best, wants to compare V3 vs V4, or wants to find the optimal fee tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, DeFi analysts, and liquidity providers use this skill to compare Uniswap pools for a token pair across protocol versions, fee tiers, TVL, volume, APY, and liquidity depth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installer examples can change what gets installed over time.

Mitigation: Install from a trusted, pinned ClawHub version or verified commit.

Risk: Pool rankings and APY or liquidity recommendations may influence financial decisions.

Mitigation: Verify pool metrics and recommendations against trusted market data before trading or providing liquidity.

Risk: Token-pair research is delegated to the configured pool-researcher.

Mitigation: Review the pool-researcher configuration and data-sharing expectations before using sensitive or private analysis inputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison table with a concise recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked pool metrics such as TVL, 24-hour volume, APY, liquidity depth, and recommendation notes.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
