## Description: <br>
Scans Uniswap deployments across chains for price differences, evaluates profitability after costs, assesses risk, and can optionally execute user-confirmed cross-chain arbitrage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DeFi operators, and wallet-enabled agents use this skill to scan for cross-chain Uniswap arbitrage opportunities, compare net profitability after gas, bridge, and slippage costs, and prepare or execute user-confirmed trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live cross-chain crypto trades and bridging. <br>
Mitigation: Use scan-only mode first and require manual wallet review and signing before every transaction. <br>
Risk: There is no clear default spending cap in the release evidence. <br>
Mitigation: Set an explicit maximum trade amount before execution and stop if the proposed amount exceeds it. <br>
Risk: Cross-chain arbitrage opportunities can expire during confirmation or bridge settlement. <br>
Mitigation: Re-check profitability immediately before execution and present net profit after gas, bridge fees, and slippage rather than gross spread. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/cross-chain-arbitrage-cn) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with opportunity tables, risk summaries, execution status, and profit-and-loss details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction identifiers, bridge order status, cost breakdowns, and scan-only recommendations when execution is not requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
