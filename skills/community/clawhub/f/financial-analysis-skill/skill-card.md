## Description:

This skill analyzes local CSV market data to run rolling-window risk parity portfolio backtests and generate text reports, JSON metrics, and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzratgit](https://clawhub.ai/user/wzratgit)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and investment researchers use this skill to evaluate multi-asset portfolio allocations from local CSV data, including rolling risk parity weights, returns, volatility, drawdown, Sharpe ratio, and asset correlations. It is intended for local analytical workflows and does not require API keys or network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CSV data may contain sensitive financial information.

Mitigation: Run the skill on non-sensitive CSVs first and keep input data and generated outputs in a dedicated local folder.

Risk: Generated reports include backtest metrics and investment-style suggestions that may be mistaken for validated financial advice.

Mitigation: Treat outputs as analytical references, review data quality and assumptions, and validate results before using them in financial decisions.

Risk: Documentation shows dependency hygiene issues between minimal dependencies and broader older commands.

Mitigation: Install in a dedicated virtual environment and use the minimal manifest or README dependency set: pandas, numpy, matplotlib, and seaborn.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wzratgit/skills/financial-analysis-skill)
- [Publisher Profile](https://clawhub.ai/user/wzratgit)
- [README](artifact/README.md)
- [Network Security Notes](artifact/NETWORK_SECURITY.md)
- [Installation Guide](artifact/INSTALLATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime output includes text reports, JSON metrics, and PNG charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to the selected local output directory, including rolling_risk_parity_report.txt, rolling_risk_parity_data.json, and rolling_*.png chart files.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
