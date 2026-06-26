## Description: <br>
Fully automated workflow for AI content monitoring and Feishu push notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianca1227](https://clawhub.ai/user/bianca1227) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an unattended workflow that watches AI content logs for ready signals, sends generated summaries or briefs to Feishu, and records processing status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended monitoring can send local file contents from log-referenced paths to Feishu. <br>
Mitigation: Restrict monitored logs and content paths to a dedicated directory, add approval or redaction for sensitive content, and review Feishu permissions before enabling automation. <br>
Risk: A default Feishu target chat can route generated content to an unintended destination. <br>
Mitigation: Replace and verify the target chat ID during setup, then test with non-sensitive content before scheduling recurring pushes. <br>
Risk: Processed files may be renamed automatically after successful delivery. <br>
Mitigation: Confirm automatic renaming is acceptable for the workflow or adjust the scripts before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianca1227/auto-push-system-skill) <br>
- [README](README.md) <br>
- [OpenClaw auto-push documentation](https://docs.openclaw.ai/skills/auto-push-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration files, cron-oriented shell scripts, logs, Feishu messages, and processed-file markers when installed and executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
