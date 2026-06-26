## Description: <br>
Checks Claude Code OAuth usage limits for session and weekly quotas, including remaining usage, rate-limit status, automated session refresh reminders, and reset detection monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azaidi94](https://clawhub.ai/user/azaidi94) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to check current OAuth session and weekly quota utilization, view reset timing, and optionally configure local reminders or polling-based notifications for quota resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Claude Code OAuth credentials to call Anthropic's usage API. <br>
Mitigation: Install and run it only in environments where that credential access is acceptable, and review the scripts before execution. <br>
Risk: The notification helper can send reset messages to a fixed Telegram target. <br>
Mitigation: Do not run or schedule monitor-and-notify.sh until the target is removed or replaced with a user-controlled destination. <br>
Risk: Reminder and monitoring scripts can create recurring Clawdbot cron jobs. <br>
Mitigation: Review created cron jobs after setup and remove jobs that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/azaidi94/claude-code-usage) <br>
- [README.md](README.md) <br>
- [CRON_SETUP.md](CRON_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text, JSON objects, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache usage output locally and can create or describe recurring notification jobs when monitoring scripts are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
