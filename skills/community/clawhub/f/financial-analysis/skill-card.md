## Description:

Analyzes multi-asset portfolios using local CSV market data, rolling inverse-volatility risk-parity style weighting, monthly rebalancing, backtesting metrics, text reports, JSON data, and PNG visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzratgit](https://clawhub.ai/user/wzratgit)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and portfolio researchers use this skill to run local rolling-window portfolio backtests on CSV return data and generate performance, risk, allocation, and correlation outputs. It is suitable for educational and analytical review, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest reports and generated investment suggestions may be mistaken for personalized financial advice.

Mitigation: Treat outputs as educational analysis only and require independent review before any investment decision.

Risk: Unpinned Python dependencies and arbitrary CSV paths can make local runs less reproducible or expose unintended files.

Mitigation: Install dependencies in a dedicated virtual environment, prefer pinned package versions, and run only on chosen CSV files.

Risk: Fixed output filenames may overwrite previous reports, JSON data, or chart files.

Mitigation: Use a dedicated output directory for each run or archive existing outputs before rerunning the skill.

Risk: The weighting logic appears to be inverse-volatility weighting rather than a full equal-risk-contribution optimizer.

Mitigation: Describe results as a risk-parity style approximation and validate methodology before using outputs for formal analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wzratgit/skills/financial-analysis)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [优化使用指南.md](artifact/优化使用指南.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [Plain-text reports, JSON metrics, PNG charts, and console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fixed report, data, and chart filenames under the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
