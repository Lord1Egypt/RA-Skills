## Description: <br>
Find and execute cross-chain arbitrage opportunities across Uniswap deployments, including scan-only reporting, cost analysis, risk assessment, and optional execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
DeFi users and developers use this skill to scan for cross-chain Uniswap price discrepancies, estimate net profitability after gas, bridge fees, and slippage, assess trade risk, and optionally execute selected arbitrage opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move wallet funds through cross-chain trades without clear default spending limits or wallet boundaries. <br>
Mitigation: Use scan-only mode first, use a limited wallet, set an explicit maxAmount, token and chain allowlists, slippage limits, and require manual wallet confirmation for every transaction. <br>
Risk: Cross-chain arbitrage opportunities can change or disappear before execution completes. <br>
Mitigation: Re-scan before acting, review the risk assessment, keep trade sizes limited, and treat projected profit as an estimate rather than a guarantee. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/cross-chain-arbitrage) <br>
- [Skill specification](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style reports with tables, warnings, confirmations, and transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scan-only opportunity reports, risk vetoes, execution progress, and profit/loss summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
