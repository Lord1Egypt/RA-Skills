## Description: <br>
A-share paper-trading automation workflow for MX APIs that sets up scheduled mock trading, risk limits, stale-order cancellation, daily reviews, and balance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youjunzhao](https://clawhub.ai/user/youjunzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading workflow operators use this skill to set up and maintain an A-share paper-trading workflow with MX APIs, scheduled strategy runs, risk caps, stale-order cancellation, and daily review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create local automation and report files, update the README, and set up trading-day runs. <br>
Mitigation: Install it only in a workspace where those file and schedule changes are acceptable, and review generated scripts, reports, and schedules before relying on them. <br>
Risk: MX API credentials used with trading automation can increase exposure if reused with real accounts. <br>
Mitigation: Use a limited MX paper-trading API key and keep the workflow separate from real trading credentials or accounts. <br>


## Reference(s): <br>
- [A-Share Claw on ClawHub](https://clawhub.ai/youjunzhao/a-share-claw) <br>
- [Publisher profile](https://clawhub.ai/user/youjunzhao) <br>
- [MX API endpoint](https://mkapi2.dfcfs.com/finskillshub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, json, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, Python files, JSON configuration, review JSON, and README table updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates mx_autotrade runtime files, scheduled-run guidance, daily review JSON, and README balance tracking in the workspace.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
