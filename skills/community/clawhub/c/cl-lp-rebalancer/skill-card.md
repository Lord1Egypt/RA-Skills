## Description: <br>
Automates Uniswap V3 concentrated-liquidity LP rebalancing on EVM L2 chains using volatility-adaptive ranges, trend-aware asymmetry, and OnchainOS-driven claim, redeem, swap, and deposit actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synththoughts](https://clawhub.ai/user/synththoughts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced DeFi operators use this skill to configure and run an agent-assisted Uniswap V3 LP rebalancer that monitors prices, computes ranges, manages positions, and reports portfolio status and performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an automated trading bot with live wallet authority. <br>
Mitigation: Use a dedicated limited-funds wallet, verify behavior manually with read-only/status commands first, and enable scheduled execution only after reviewing the configured pool and wallet permissions. <br>
Risk: The skill can send notifications and query balances across external services when those settings or credentials are present. <br>
Mitigation: Configure Discord, Telegram, Binance, and Hyperliquid variables only when those integrations are intended, and avoid shared notification destinations for private portfolio data. <br>
Risk: Automated swaps, liquidity removal, and deposits can lose funds through market movement, slippage, gas costs, or failed transactions. <br>
Mitigation: Keep slippage, gas, stop-loss, rebalance-frequency, and circuit-breaker controls enabled, and monitor state after initial deployment and failed rebalance attempts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/synththoughts/cl-lp-rebalancer) <br>
- [README](README.md) <br>
- [Range Algorithm Documentation](references/range-algorithm.md) <br>
- [Reference configuration](references/config.json) <br>
- [Rebalancer implementation](references/cl_lp.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON notification blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live wallet-changing DeFi actions when configured with credentials; status output can use a five-minute cache.] <br>

## Skill Version(s): <br>
3.9.2 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
