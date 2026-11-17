## Description:

跨链套利 | Cross-Chain Arbitrage. Uniswap 跨链套利机会 | Uniswap cross-chain arbitrage. 发现不同链上的价格差异 | Find price differences across chains. 触发词：跨链、套利、Uniswap、arbitrage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to scan Uniswap deployments across chains for token price discrepancies, estimate profitability after gas, bridge fees, and slippage, and optionally execute a risk-gated arbitrage workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real on-chain fund movement during cross-chain arbitrage execution.

Mitigation: Install only from a reviewed fixed version or commit, avoid broad wallet permissions, set explicit maximum trade amounts, and require user confirmation before any swap or bridge.

Risk: Arbitrage opportunities are time-sensitive, so price movement during bridge settlement can erase projected profit or create a loss.

Mitigation: Use scan-only mode first, present all-in costs rather than gross spread, re-check profitability near execution, and warn users that actual profit may differ.

Risk: Bridge liquidity, settlement delays, or smart contract issues can prevent safe completion.

Mitigation: Run the documented safety and balance checks, use the risk-assessor gate, veto insufficient-liquidity routes, and report bridge delays or failures clearly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/cross-chain-arbitrage-cn)
- [ClawHub metadata link](https://clawhub.ai)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, status updates, confirmation prompts, and inline shell commands for installation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scan-only reports, risk-veto reports, execution progress updates, and final profit-and-loss summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
