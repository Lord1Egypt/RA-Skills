## Description: <br>
Run Freqtrade backtests for cryptocurrency trading strategies, interpret results, and iterate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to download Freqtrade market data, run cryptocurrency strategy backtests, interpret result metrics, compare strategy variants, and decide whether a strategy is ready for cautious live testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest commands can be run with the wrong Docker Compose setup, exchange, pair, timeframe, or timerange. <br>
Mitigation: Review the docker-compose setup and command parameters before execution. <br>
Risk: Live exchange API keys could expose funds if they are reused during testing. <br>
Mitigation: Avoid live exchange API keys unless they are tightly permissioned and withdrawals are disabled. <br>
Risk: A strategy that performs well in historical backtests may fail in live markets or be overfit to one period. <br>
Mitigation: Compare fixed-period baselines, change one parameter at a time, test multiple market conditions, and start any live trial with small position sizes. <br>


## Reference(s): <br>
- [Reading Backtest Results](references/reading-results.md) <br>
- [Iteration Guide](references/iteration-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/freqtrade-backtester) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Freqtrade Docker commands, environment variable guidance, and interpretation guidance for backtest results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
