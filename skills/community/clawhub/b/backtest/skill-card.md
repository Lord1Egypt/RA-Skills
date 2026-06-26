## Description: <br>
Runs A-share strategy backtests with AkShare market data and writes CSV equity-curve and trade records for reviewing historical performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gracexiaoo](https://clawhub.ai/user/gracexiaoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and developers use this skill to run historical A-share strategy backtests with configurable capital and date ranges. It helps compare simulated returns, drawdowns, win rate, and trade records before any separate investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest output can be incomplete or misleading if market data is unavailable, assumptions are optimistic, or results are treated as investment advice. <br>
Mitigation: Treat results as informational, review strategy assumptions and CSV outputs, and make investment decisions outside the skill. <br>
Risk: Running the skill installs Python packages, makes network calls for market data, and writes CSV files locally. <br>
Mitigation: Install dependencies in a Python virtual environment, expect outbound data requests, and review the configured output directory before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gracexiaoo/backtest) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints a backtest summary and writes daily values and trade records to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
