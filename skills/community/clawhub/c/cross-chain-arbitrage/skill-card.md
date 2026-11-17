## Description:

Find and execute cross-chain arbitrage opportunities by scanning Uniswap prices across chains, calculating net profitability after gas, bridge fees, and slippage, assessing risk, and supporting scan-only research mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to scan for token price discrepancies across Uniswap chains, evaluate expected profit after gas, bridge fees, and slippage, and either review opportunities in scan-only mode or confirm risk-gated execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-chain arbitrage can spend funds through on-chain transactions that may be irreversible.

Mitigation: Use scan-only mode unless ready to approve real transactions, and confirm the route, amount, chain, costs, slippage, bridge risk, and worst-case loss before execution.

Risk: Arbitrage opportunities can disappear before or during bridge settlement, reducing profit or creating a loss.

Mitigation: Re-scan close to execution time, review the skill's time-sensitivity warnings, and proceed only after the risk assessment and user confirmation steps.

Risk: Bridge, liquidity, slippage, or smart contract conditions can make an opportunity unsafe.

Mitigation: Rely on the documented risk-assessment gate and stop when the workflow returns VETO or HARD_VETO.

Risk: Installing an untrusted or changed release can expose users to unsafe behavior.

Mitigation: Install only from trusted sources and prefer pinned package versions or reviewed commits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/cross-chain-arbitrage)
- [Publisher profile](https://clawhub.ai/user/wpank)
- [Skill specification](artifact/SKILL.md)
- [Readme](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, confirmation prompts, and transaction status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scan-only reports, risk veto summaries, execution progress, and profit-and-loss reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
