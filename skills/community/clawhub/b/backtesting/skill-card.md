## Description: <br>
Helps agents design and interpret Superior Trade backtests, including window selection, trade-count thresholds, parameter sweeps, walk-forward checks, zero-trade diagnosis, and compute-cost expectations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate whether Superior Trade backtest results are reliable before iterating on strategy parameters or considering deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtesting guidance may influence trading decisions or be mistaken for financial advice. <br>
Mitigation: Treat outputs as analytical guidance, keep human control over live deployment, and do not present backtest results as financial advice. <br>
Risk: Thin, cherry-picked, or overfit backtests can create misleading confidence. <br>
Mitigation: Use meaningful windows, require adequate trade counts, and perform out-of-sample walk-forward checks before acting on results. <br>
Risk: Large backtests can consume paid compute or take longer than expected. <br>
Mitigation: Estimate candle count before submission, warn users about long runs, and use slower polling cadence for large jobs. <br>


## Reference(s): <br>
- [Backtesting ClawHub Release](https://clawhub.ai/superior-ai/backtesting) <br>
- [Superior Trade Backtest Workflow](https://github.com/Superior-Trade/superior-skills/blob/main/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with tables, diagnostic steps, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only; no executable code or hidden data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
