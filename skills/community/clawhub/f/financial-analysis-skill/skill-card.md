## Description: <br>
Runs offline multi-asset portfolio risk-parity analysis, rolling rebalancing backtests, and report/chart generation from local CSV market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzratgit](https://clawhub.ai/user/wzratgit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Financial analysts, developers, and agent users can use this skill to evaluate local CSV market data with rolling risk-parity backtests and generate portfolio performance metrics, reports, and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stale documentation may suggest installing or using dependencies that are not needed for this offline release. <br>
Mitigation: Install only the dependencies listed in the manifest or README and ignore the stale yfinance example in SKILL.md. <br>
Risk: Generated reports can include local file paths and financial analysis results. <br>
Mitigation: Use non-sensitive CSV data for testing and review generated reports before sharing them. <br>
Risk: The skill writes reports, JSON data, and charts to a local output directory. <br>
Mitigation: Choose a dedicated empty output directory before running the backtest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzratgit/financial-analysis-skill) <br>
- [README.md](artifact/README.md) <br>
- [NETWORK_SECURITY.md](artifact/NETWORK_SECURITY.md) <br>
- [INSTALLATION.md](artifact/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, shell commands, guidance] <br>
**Output Format:** [Plain text reports, JSON data files, PNG charts, and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local CSV path and writes reports and charts to a chosen local output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
