## Description: <br>
Schedule and run safe daily or weekly updates for Clawdbot and installed skills using the Gateway cron scheduler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xabo1986](https://clawhub.ai/user/xabo1986) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure recurring Clawdbot Gateway cron jobs that report on, and optionally apply, ClawHub skill and Clawdbot updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent scheduled job that updates all installed skills. <br>
Mitigation: Review the cron schedule before installation, start in report-only mode, and confirm how to list, pause, or delete the cron job. <br>
Risk: Optional Clawdbot self-updates and restarts can disrupt running automation. <br>
Mitigation: Require explicit manual approval before enabling self-updates or restarts, schedule changes during a quiet window, and run doctor checks after updates. <br>
Risk: The sample command contains absolute local paths and a hard-coded Telegram recipient. <br>
Mitigation: Replace all absolute paths and notification recipients with environment-specific values before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xabo1986/auto-updater-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/xabo1986) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples and cron configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for Clawdbot cron scheduling, ClawHub login checks, update reporting, and optional self-update workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
