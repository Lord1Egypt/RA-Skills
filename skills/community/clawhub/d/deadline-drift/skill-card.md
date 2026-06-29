## Description: <br>
Use when a Polymarket market probability changes as the resolution deadline approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy agents use this skill to assess Polymarket markets where time remaining is central to the thesis, backtest deadline-related price drift, and configure cautious entry and exit timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deadline-based probability drift can be overwhelmed by event-driven jumps or market-rule interpretation issues. <br>
Mitigation: Backtest on filled TradeTicks, confirm market metadata and resolution terms, and use conservative sizing before acting on the strategy. <br>
Risk: Holding through settlement can create binary exposure unrelated to interim price movement. <br>
Mitigation: Use an exit buffer before market close unless the user explicitly chooses settlement exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/deadline-drift) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Analysis] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Strategy guidance emphasizes filled TradeTick backtesting, deadline windows, drift thresholds, position sizing, and exit buffers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
