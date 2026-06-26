## Description: <br>
Automated liquidity provision optimizer for CLMM DEXs on Solana and Ethereum that compares APR yields, estimates impermanent loss risk, scores pool safety by TVL, and recommends rebalancing for out-of-range positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi analysts can use this skill to compare concentrated liquidity pools, estimate impermanent loss scenarios, and generate risk-adjusted liquidity provision guidance across Solana and Ethereum protocols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses mock pool data and may produce misleading yield comparisons if treated as live market data. <br>
Mitigation: Use it only for local inspection until mock data is replaced with verified live market data from trusted pool APIs. <br>
Risk: Security guidance flags reliability flaws in the impermanent loss calculation and TVL display that can affect allocation decisions. <br>
Mitigation: Fix and validate those calculations before relying on recommendations for real DeFi allocation decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and plain-text CLI reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mock pool data unless integrated with verified live pool APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
