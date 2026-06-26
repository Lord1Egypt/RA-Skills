## Description: <br>
A-share quantitative strategy backtesting tool that uses AkShare historical market data to simulate strong-stock rotation strategies and output equity curves, trade records, and monthly statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gracexiaoo](https://clawhub.ai/user/gracexiaoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run local historical backtests for A-share short-term stock strategies, review simulated trades, and inspect CSV performance outputs. The results are experimental financial analysis and are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest results may be mistaken for investment advice or future performance guarantees. <br>
Mitigation: Treat outputs as experimental financial analysis only and review assumptions before using results in any decision process. <br>
Risk: AkShare retrieves market data and strategy controls may be hardcoded or differ from the documentation. <br>
Mitigation: Review the script, dependencies, and configured parameters before relying on generated performance metrics. <br>
Risk: The skill writes CSV outputs to a local directory. <br>
Mitigation: Run it in an expected workspace and choose an output path that is safe to create or overwrite. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gracexiaoo/akshare-backtest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Analysis, Guidance] <br>
**Output Format:** [Command-line output plus CSV files and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes backtest result CSV files to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
