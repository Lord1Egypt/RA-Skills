## Description:

波龙股神量化交易系统 helps agents support A-share and futures quantitative workflows, including factor-based stock screening, backtesting, QMT and Wenhua execution commands, and risk monitoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonstang](https://clawhub.ai/user/simonstang)

### License/Terms of Use:

MIT

## Use Case:

Developers, quantitative-trading practitioners, and external users can use this skill to ask an agent for setup commands, configuration guidance, stock-screening workflows, backtest report generation, broker execution commands, and risk-monitoring procedures for A-share and futures trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broker credential handling and commands that can place real-money trades.

Mitigation: Review before installing, run in an isolated environment, keep real broker credentials out of checked-in config files, and avoid live mode unless confirmations and order limits are added.

Risk: Generated stock picks and backtest reports may be misleading if the data path or calculations are not independently verified.

Mitigation: Treat generated picks and backtests as demos until data sources, assumptions, and calculations are reviewed against trusted records.

Risk: Telegram alerting can send account, position, or trading alert data to a configured chat.

Mitigation: Disable Telegram unless that data sharing is acceptable, and protect push tokens and chat identifiers as secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonstang/skills/bowlong-quant-aio)
- [V2.1 optimization notes](artifact/docs/OPTIMIZATION_V2.1.md)
- [Project homepage](https://learn2study.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code blocks, shell commands, configuration snippets, CSV or JSON output paths, and generated report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated stock-pick CSV files, backtest reports, risk-monitoring reports, and trading command examples.]

## Skill Version(s):

2.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
