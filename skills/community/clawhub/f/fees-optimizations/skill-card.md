## Description: <br>
Helps agents reason about Hyperliquid and Superior trading costs, slippage, maker versus taker execution, and Freqtrade configuration choices for cost-sensitive deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, trading operators, and agents use this skill to analyze fee drag, slippage, and maker-versus-taker tradeoffs before recommending Hyperliquid Freqtrade configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill's trading and stop-loss guidance as authoritative risk-management advice for live or leveraged trading. <br>
Mitigation: Treat the skill as fee-analysis reference material, verify stop-loss behavior against current Freqtrade, Hyperliquid, and Superior documentation, and test changes outside live leveraged trading before deployment. <br>
Risk: Fee, builder-code, and slippage assumptions can become stale or differ by account and market. <br>
Mitigation: Check current Hyperliquid fee tier, Superior builder-code rate, and filled-order slippage before relying on any cost estimate. <br>


## Reference(s): <br>
- [Hyperliquid Fees](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees) <br>
- [Hyperliquid Portfolio](https://app.hyperliquid.xyz/portfolio) <br>
- [Freqtrade Order Types Configuration](https://www.freqtrade.io/en/stable/configuration/#understand-order_types) <br>
- [Freqtrade Entry and Exit Pricing Configuration](https://www.freqtrade.io/en/stable/configuration/#understand-entry_pricing-and-exit_pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes fee-analysis heuristics, source-of-truth checks, and Freqtrade configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
