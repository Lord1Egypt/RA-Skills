## Description: <br>
Monitors daily report cron health and sends independent Feishu alerts when recent failures, delivery issues, or missing report files are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colbertlee](https://clawhub.ai/user/colbertlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to add an application-level watchdog for daily report cron jobs. It checks recent OpenClaw cron status, expected report files, cooldown state, and Feishu alert delivery without relying only on platform failure alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu alerts may include operational details such as cron status, diagnostics, timestamps, and file paths. <br>
Mitigation: Configure the Feishu destination deliberately and avoid including secrets or sensitive paths in alert payloads. <br>
Risk: Scheduled alerting can notify the wrong channel or run more often than intended if cron behavior is not reviewed. <br>
Mitigation: Confirm the Feishu account, recipient, cooldown, and every-30-minute schedule before deployment. <br>
Risk: The watcher is configured for a specific daily report job and workspace path. <br>
Mitigation: Set the job ID, workspace path, report directory, and sender configuration for the target environment before installing the cron job. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/colbertlee/daily-report-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/colbertlee) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Watcher script](artifact/watcher.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples plus runtime console text and Feishu alert content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes 0, 1, and 2 indicate normal status, detected issue, and check error states.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and user changelog, released 2026-06-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
