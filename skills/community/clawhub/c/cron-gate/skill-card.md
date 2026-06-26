## Description: <br>
Cron Gate is a local Python helper that checks OpenClaw session activity before triggering configured cron jobs so idle sessions do not start costly LLM work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ori-claw](https://clawhub.ai/user/ori-claw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators running OpenClaw use this skill to install and configure a lightweight cron gate that runs cheap local activity checks before triggering selected LLM cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured session-to-cron mappings could trigger unintended OpenClaw cron jobs. <br>
Mitigation: Review and edit SESSION_CRONS carefully, configure only intended cron IDs, and run --dry-run before enabling scheduled execution. <br>
Risk: The state and log files can reveal activity timing for configured sessions. <br>
Mitigation: Run the script as the normal OpenClaw user and protect the state and log files with appropriate local file permissions. <br>
Risk: Leaving system crontab entries active after the workflow is no longer needed could continue triggering configured jobs. <br>
Mitigation: Remove the crontab entries when you stop using Cron Gate. <br>


## Reference(s): <br>
- [Cron Gate ClawHub release](https://clawhub.ai/ori-claw/cron-gate) <br>
- [Publisher profile](https://clawhub.ai/user/ori-claw) <br>
- [Artifact documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for local cron configuration; the included helper script makes localhost API calls when configured and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
