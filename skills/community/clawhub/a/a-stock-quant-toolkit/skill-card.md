## Description:

Provides an A-share quantitative analysis toolkit for real-time Tencent market data, technical indicators, strategy backtesting, monitoring scores, FFT cycle analysis, and daily report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to have an agent generate A-share market analysis workflows, technical indicator calculations, backtest comparisons, monitoring summaries, and daily market reports. Results should be reviewed as decision support rather than relied on as trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hidden local-code bridges or alert synchronization can execute or connect to local integrations outside the core finance workflow.

Mitigation: Remove or disable the python_bridge.py execution path and system_bridge alert sync unless those integrations are explicitly required and trusted.

Risk: Market data is fetched from external Tencent and Sina endpoints, including unauthenticated HTTP paths, so outputs may be unavailable, stale, or affected by transport and source integrity issues.

Mitigation: Use trusted data feeds for production decisions, validate fetched data before acting on it, and avoid using the toolkit as the sole basis for trading.

Risk: Generated scores, backtests, reports, and strategy signals can be misleading if market assumptions, data quality, or parameters are wrong.

Mitigation: Treat all finance output as decision-support analysis, review calculations independently, and require human approval before any trade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dnaxxx-hub/skills/a-stock-quant-toolkit)
- [Publisher profile](https://clawhub.ai/user/dnaxxx-hub)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python examples, command snippets, and structured finance analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market summaries, indicator values, strategy rankings, backtest metrics, monitoring alerts, and report text.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
