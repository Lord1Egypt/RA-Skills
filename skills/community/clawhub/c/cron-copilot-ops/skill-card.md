## Description: <br>
Install, configure, and operate CronCopilot, a Python-based scheduled task management system for cron jobs, scripts, monitoring, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eden2f](https://clawhub.ai/user/eden2f) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to install CronCopilot, configure scheduled tasks, manage scripts, monitor execution history, and troubleshoot scheduler failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent through local scheduler setup, daemon control, task removal, and script deletion operations that can affect host availability or remove files. <br>
Mitigation: Run under a least-privileged account, register only trusted scripts, and require explicit confirmation before service setup, forced task removal, or script deletion with --delete-file. <br>
Risk: CronCopilot alert configuration can include SMTP credentials in local config files. <br>
Mitigation: Protect configuration files, avoid exposing SMTP passwords in chat or logs, and rotate credentials if they are shared inadvertently. <br>


## Reference(s): <br>
- [CronCopilot Skill Page](https://clawhub.ai/eden2f/cron-copilot-ops) <br>
- [CronCopilot GitHub Repository](https://github.com/eden2f/cron-copilot) <br>
- [CronCopilot Gitee Repository](https://gitee.com/eden2f/cron-copilot) <br>
- [CronCopilot Detailed Reference](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for CronCopilot setup, task management, monitoring, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
