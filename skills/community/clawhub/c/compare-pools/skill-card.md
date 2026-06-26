## Description: <br>
Compare all Uniswap pools for a token pair across fee tiers and versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DeFi analysts, and liquidity providers use this skill to compare Uniswap pools for a token pair across protocol versions, fee tiers, and chains. It helps rank candidate pools by TVL, volume, APY, liquidity depth, and related tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pool comparisons may rely on public DeFi data gathered by the delegated pool-researcher subagent. <br>
Mitigation: Confirm that public DeFi data lookups are acceptable for the intended environment before installing or using the skill. <br>
Risk: Rankings and recommendations can become stale as liquidity, volume, APY, and depth change over time. <br>
Mitigation: Use current pool data for each comparison and review the recommendation before making liquidity provision or trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/compare-pools) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison table with a concise recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pool rankings by TVL, volume, APY, liquidity depth, fee tier, protocol version, and chain.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
