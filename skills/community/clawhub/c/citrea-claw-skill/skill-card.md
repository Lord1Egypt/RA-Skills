## Description:

Run Citrea L2 monitoring commands to check arbitrage opportunities, token prices, pool liquidity, wallet balances, and new pools across JuiceSwap and Satsuma DEXes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-chew](https://clawhub.ai/user/jason-chew)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, liquidity providers, and developers active on Citrea use this skill to ask an agent for Citrea DeFi monitoring, wallet checks, liquidity views, arbitrage scans, and optional Telegram alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run local Node commands with user-provided arguments.

Mitigation: Review or pin the source before installation and validate or quote user-provided command arguments before execution.

Risk: Telegram bot credentials may be stored in plaintext configuration.

Mitigation: Avoid pasting tokens into chat when possible and store secrets in files with restrictive permissions.

Risk: Arbitrage output is indicative and may be stale before any trade is executed.

Mitigation: Verify prices and opportunities on-chain before acting on any arbitrage result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-chew/skills/citrea-claw-skill)
- [Citrea](https://citrea.xyz)
- [Citrea mainnet RPC](https://rpc.mainnet.citrea.xyz)
- [Citrea mainnet explorer](https://explorer.mainnet.citrea.xyz)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live on-chain values, wallet addresses, token symbols, pool data, arbitrage summaries, and Telegram alert setup guidance.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
