## Description: <br>
Analyzes multi-asset portfolios with rolling-window risk-parity backtests, CSV data ingestion, performance metrics, text reports, and chart outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzratgit](https://clawhub.ai/user/wzratgit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and portfolio researchers use this skill to run local risk-parity backtests from trusted CSV market-return data and generate portfolio allocation, return, risk, and correlation outputs. The outputs support analysis and review, not personalized financial advice or proof of future returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local CSV files and writes reports, derived JSON, and charts to local output paths. <br>
Mitigation: Run it in a virtual environment and use only CSV and output paths you trust. <br>
Risk: Generated reports may include local file paths and derived portfolio data. <br>
Mitigation: Review reports and charts before sharing them outside the intended audience. <br>
Risk: Backtest metrics and investment suggestions can be mistaken for personalized financial advice or future-performance evidence. <br>
Mitigation: Treat outputs as informational research and validate assumptions, transaction costs, and data quality before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzratgit/financial-analysis) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [优化使用指南.md](artifact/优化使用指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance plus generated TXT, JSON, and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads CSV input paths and writes reports, derived data, and charts to a chosen output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
