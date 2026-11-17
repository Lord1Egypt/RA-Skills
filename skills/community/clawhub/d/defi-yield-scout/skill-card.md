## Description:

Scan and compare USDC yield farming APYs on Base and Arbitrum, analyze vault performance, breakeven migration, and protocol risk using live DeFiLlama data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaoolucas](https://clawhub.ai/user/joaoolucas)

### License/Terms of Use:


## Use Case:

Developers, DeFi analysts, and agent operators use this skill to compare USDC yield opportunities, inspect APY history, evaluate migration breakeven, and review supported protocol risk notes before making independent decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared temporary cache could let a local attacker tamper with yield results or overwrite writable files.

Mitigation: Review before installing on shared machines and prefer a version that stores cache files in a private per-user directory with symlink and ownership checks.

Risk: The skill output may influence financial decisions using point-in-time APY data and approximate gas or bridge costs.

Mitigation: Verify APYs, TVL, pool details, protocol risk, gas, bridge costs, and on-chain conditions independently before moving funds.

## Reference(s):

- [Protocol Reference](artifact/references/protocols.md)
- [DeFiLlama Yield Pools API](https://yields.llama.fi/pools)
- [DeFiLlama Yield Pool Chart API](https://yields.llama.fi/chart/{pool_id})
- [ClawHub Skill Page](https://clawhub.ai/joaoolucas/skills/defi-yield-scout)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, analysis, guidance]

**Output Format:** [Markdown tables and prose, with optional JSON output from the CLI tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live DeFiLlama data and a 15-minute local cache; APYs and gas estimates are informational snapshots.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
