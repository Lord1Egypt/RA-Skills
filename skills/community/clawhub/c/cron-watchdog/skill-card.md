## Description: <br>
Monitor all OpenClaw cron jobs for failures and auto-fix common errors such as model-not-allowed errors and timeouts, posting to Slack only when issues are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpbshhx](https://clawhub.ai/user/mpbshhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw cron job health, apply common automated remediations, and send Slack alerts only when cron issues need attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify and force-run cron jobs without an explicit approval step. <br>
Mitigation: Use an explicit job allowlist, require approval before updates or force-runs, log every change, and send alerts to an appropriate operational Slack channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mpbshhx/cron-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Agent tool calls and concise Slack status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a recurring schedule and remains silent when no cron issues are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
