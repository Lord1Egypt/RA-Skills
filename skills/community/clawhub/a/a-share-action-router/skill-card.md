## Description: <br>
Routes fresh A-share market context, calibrated portfolio inputs, and user constraints into ordered keep, trim, exit, and add decisions with target allocation and next-day scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minguncle](https://clawhub.ai/user/minguncle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn current A-share market workups, calibrated holdings, and personal constraints into an ordered portfolio action plan. It is intended for decision support, including scenario-based next-day execution guidance, not account access or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outdated market data, incomplete holdings, or unclear screenshot timestamps can lead to misleading portfolio actions. <br>
Mitigation: Require fresh market inputs, calibrated portfolio details, and explicit timestamps or assumptions before providing final action guidance. <br>
Risk: Portfolio planning guidance may be mistaken for brokerage execution or account-specific financial advice. <br>
Mitigation: Use the skill only as decision support, keep trade execution outside the skill, and never provide brokerage credentials or account-identifying details. <br>
Risk: Concentrated or abrupt position changes can create avoidable trading risk. <br>
Mitigation: Apply the skill's hard rules requiring trigger conditions, invalidation conditions, position rationale, core risks, and avoidance of all-in or full-rotation recommendations. <br>


## Reference(s): <br>
- [Router Template](references/router-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown action plan with tables, ordered steps, scenario bullets, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires fresh market context and calibrated portfolio inputs before final portfolio actions; does not install code, access accounts, or execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
