## Description: <br>
Expert guidance for systematic backtesting of trading strategies, including parameter robustness testing, slippage modeling, bias prevention, and interpretation of backtest results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quantitative researchers, and trading-system builders use this skill to structure backtest validation, identify fragile strategy results, and decide whether a strategy needs refinement before any live-trading consideration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest scores or Deploy/Refine/Abandon verdicts may create false confidence in a strategy. <br>
Mitigation: Treat outputs as educational research guidance and require independent review, out-of-sample testing, execution-cost modeling, and risk approval before any live trading. <br>
Risk: The optional Python script writes local report files and may be run on user-supplied metrics. <br>
Mitigation: Review the script before execution and run it in a controlled workspace with an explicit output directory. <br>
Risk: The skill evaluates trading-strategy validation quality but does not prove profitability or safety. <br>
Mitigation: Use it as a structured screening framework, not as financial advice, a trading signal, or broker-execution automation. <br>


## Reference(s): <br>
- [Backtesting Methodology Reference](references/methodology.md) <br>
- [Learning from Failed Backtests](references/failed_tests.md) <br>
- [ClawHub release page](https://clawhub.ai/clawdiri-ai/einstein-research-backtest-dv) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clawdiri-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Natural-language guidance with optional Markdown examples, Python code, and local evaluation report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Python evaluation script can write local JSON and Markdown reports under a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
