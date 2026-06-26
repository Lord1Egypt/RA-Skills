## Description: <br>
Analyzes event-driven trading opportunities around earnings, mergers, policy changes, product approvals, litigation, and management changes, then returns JSON trading signals with risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmaya](https://clawhub.ai/user/hmaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market-analysis agents use this skill to evaluate upcoming corporate or market events, compare expectations against modeled assumptions, and generate event-driven trading analysis, signals, and risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce actionable buy/sell-style trading suggestions from simulated or externally dependent data. <br>
Mitigation: Verify market data, event timing, and assumptions independently before using the output in investment decisions. <br>
Risk: Outputs could be misused as automated trading instructions. <br>
Mitigation: Keep a human review step between this skill's recommendations and any trading or order-entry workflow. <br>
Risk: Recommended companion skills may affect the data and event context used by this skill. <br>
Mitigation: Review and approve companion skills such as MDL_data_skill and policy_analysis_skill before enabling them together. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hmaya/event-driven-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response containing event analysis, trading signals, execution plans, monitoring requirements, and risk assessment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses caller-provided JSON action parameters; outputs are advisory and require independent market-data verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact script) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
