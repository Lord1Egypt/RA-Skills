## Description: <br>
Send SMTP email notifications after Codex completes a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caopulan](https://clawhub.ai/user/caopulan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send task-completion notifications with device name, project name, status, and summary through their configured SMTP provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries, device names, project names, status, and task titles are sent through the configured SMTP provider to the configured recipients. <br>
Mitigation: Use only approved recipients and keep summaries free of secrets or sensitive details. <br>
Risk: SMTP credentials and recipient settings are provided through environment variables and could be misconfigured. <br>
Mitigation: Use app-specific SMTP credentials when possible, configure TLS or SSL appropriately, and run the helper with --dry-run before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caopulan/email-notify) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [send_email_notification.py](artifact/scripts/send_email_notification.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with environment variable examples and a Python helper invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can send SMTP email or print a dry-run preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
