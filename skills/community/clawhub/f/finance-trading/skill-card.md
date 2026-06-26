## Description: <br>
Implements a BTC/USDT paper trading strategy using EMA 20/50 crossovers and RSI signals with fixed paper-trading risk controls and trade logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brioche-bit](https://clawhub.ai/user/Brioche-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-tool users can use this skill to guide an agent through a paper-trading workflow for BTC/USDT analysis, simulated position sizing, journal updates, and daily performance reporting. It is intended for simulated trading and should not be granted live exchange authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow could be mistaken for live trading guidance or connected to real exchange authority. <br>
Mitigation: Keep the agent in paper mode and do not grant exchange credentials or live-trading permissions. <br>
Risk: Local trading journals and daily reports may be written to an unexpected location. <br>
Mitigation: Confirm where logs such as trading_log.md will be created before running the workflow. <br>
Risk: Trading signals depend on market data quality and may be misleading if the data source is unreliable. <br>
Mitigation: Use a trusted market-data source and review generated analysis before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Brioche-bit/finance-trading) <br>
- [Publisher profile](https://clawhub.ai/user/Brioche-bit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local trade journal entries and daily paper-trading performance summaries when an agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
