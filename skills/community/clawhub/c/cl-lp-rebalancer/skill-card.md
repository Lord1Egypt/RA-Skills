## Description:

Uniswap V3 concentrated-liquidity LP automation skill that uses volatility-adaptive range sizing, trend-aware asymmetric ranges, and an onchainos-driven claim, remove, swap, and deposit workflow for EVM L2 LP management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synththoughts](https://clawhub.ai/user/synththoughts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to monitor and rebalance Uniswap V3 concentrated-liquidity positions on EVM L2 networks. It supports pool setup, position status, market analysis, scheduled rebalancing, daily reporting, and manual close or reset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move funds through unattended DeFi operations.

Mitigation: Use a dedicated wallet with limited funds and avoid unattended cron execution until transaction validation and confirmation gates are reviewed.

Risk: Wallet approvals and credentials may create broad exposure if reused across accounts or left active after testing.

Mitigation: Provide only dedicated least-privilege credentials, use a dedicated wallet, and revoke token allowances after testing.

Risk: Dry-run mode should not be treated as a complete safety boundary for live trading workflows.

Mitigation: Review generated transactions and operational settings before enabling live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synththoughts/skills/cl-lp-rebalancer)
- [README.md](README.md)
- [range-algorithm.md](references/range-algorithm.md)
- [config.json](references/config.json)
- [test_triggers.py](references/test_triggers.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, configuration JSON, terminal text, and structured JSON events with optional notification payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces status summaries, analysis reports, rebalance decisions, risk alerts, daily reports, and command guidance for onchainos-based LP workflows.]

## Skill Version(s):

3.9.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
