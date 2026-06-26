## Description: <br>
Agent workspace for researching programmatic trading strategies through generative optimization with bounded files and fixed backtesting evaluator. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[lavapapa](https://clawhub.ai/user/lavapapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to set up a bounded coding-agent workspace for historical trading-strategy research, run fixed-evaluator backtests, and record strategy experiments without moving into live trading or account-connected workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch autonomous coding agents and generated Python with broad shell and edit authority. <br>
Mitigation: Install and run it only in a clean, isolated workspace with no sensitive files, broker sessions, exchange keys, or other credentials available. <br>
Risk: Generated strategies and repeated backtests can overfit historical data or produce misleading financial conclusions. <br>
Mitigation: Treat every backtest as research evidence only, report failed experiments, avoid profit claims, and do not use the skill for live trading or account-connected workflows. <br>
Risk: Automatic market-data fallbacks may reduce reproducibility or introduce dependency and network variability. <br>
Mitigation: Prefer reviewed, pinned local datasets when reproducibility matters, and review generated strategy.py before running backtests. <br>


## Reference(s): <br>
- [AutoTradeResearch repository](https://github.com/lavapapa/AutoTradeResearch) <br>
- [ClawHub skill page](https://clawhub.ai/lavapapa/autotraderesearch) <br>
- [AutoResearch inspiration](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and Python code changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained to research setup, strategy notes, generated backtest summaries, and bounded workspace edits.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
