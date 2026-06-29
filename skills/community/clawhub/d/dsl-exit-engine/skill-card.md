## Description: <br>
Helps agents design or tune Freqtrade exit logic for Superior Trade using a three-phase DSL with an ROI ladder, hard stoploss, and ratcheting trailing stop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy builders use this skill to specify and tune Freqtrade exit behavior for Superior Trade strategies. It is intended to guide configuration and strategy composition, not to guarantee trading performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-strategy guidance can be mistaken for financial advice or a safety guarantee. <br>
Mitigation: Treat generated strategy changes as guidance only; confirm scope, budget limits, risk controls, and exit rules before using them with real funds. <br>
Risk: Exit parameters can produce losses or blocked positions if applied without validation or without timeout safeguards. <br>
Mitigation: Run backtests and parameter sweeps before deployment, and pair maker-first exits with explicit unfilled-timeout settings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown with YAML, Python, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trading guidance should be reviewed and backtested before live use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
