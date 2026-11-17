## Description:

A-share quantitative backtesting skill that uses AkShare market data to run a short-term rotation strategy and report portfolio performance, trades, and monthly statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gracexiaoo](https://clawhub.ai/user/gracexiaoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run historical A-share strategy backtests, inspect simulated trade records, and compare portfolio performance over a configurable date range. Results are for research and evaluation, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest output can be mistaken for investment advice or a predictor of future market performance.

Mitigation: Treat results as research, independently validate assumptions, and avoid using the output for live trading decisions without separate financial review.

Risk: Python dependencies are not pinned, so future package changes could alter behavior or installation results.

Mitigation: Install in an isolated Python environment and pin reviewed versions of akshare, pandas, and numpy before repeated or production-like use.

Risk: The script writes CSV results to the selected output directory.

Mitigation: Run with a dedicated output directory and review generated files before sharing or reusing them.

Risk: Some documented strategy settings and output filenames differ from the script behavior.

Mitigation: Inspect the script parameters and generated filenames before relying on the documented defaults or comparing runs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python command examples, console summaries, and CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes dragon_lowpick_daily.csv and dragon_lowpick_trades.csv to the configured output directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
