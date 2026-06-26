## Description: <br>
Monitors OpenClaw context-window usage, warns when usage approaches configured thresholds, and describes automatic compression of older conversation context while preserving recent rounds and key memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhui435](https://clawhub.ai/user/yuhui435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor context-window usage, configure warning and critical thresholds, and keep long-running work responsive through context compression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic context compression may summarize or omit older conversation details. <br>
Mitigation: Confirm the compression behavior before installation, keep separate notes for important work, or disable automatic compression until the preserved context is understood. <br>
Risk: Scheduled monitoring can run repeatedly if cron scheduling is enabled. <br>
Mitigation: Review the cron command and configured check interval before enabling automated execution. <br>


## Reference(s): <br>
- [Context Monitor on ClawHub](https://clawhub.ai/yuhui435/context-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with PowerShell, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes threshold settings, scheduling commands, log examples, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
