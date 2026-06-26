## Description: <br>
Automates scheduled health checks, remediation, cleanup, backups, improvement analysis, upgrade checks, and security audits for an OpenClaw environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run recurring OpenClaw maintenance jobs for diagnosis, repair, backup, security review, and operational reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled jobs may continue changing system or workspace state after installation. <br>
Mitigation: Review the cron entries before enabling them and document a clear removal path for every installed job. <br>
Risk: Backup behavior can copy sensitive OpenClaw configuration, including environment files. <br>
Mitigation: Exclude, encrypt, or tightly restrict backups of secret-bearing files before running the backup task. <br>
Risk: Workspace-wide git staging and commits can capture unintended files. <br>
Mitigation: Replace broad git staging with a narrow allowlist of files that are safe to commit. <br>
Risk: Slack notifications may expose operational details from logs or local paths. <br>
Mitigation: Disable or minimize notifications and verify that outbound messages do not contain sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/evomasterscheduler) <br>
- [Publisher profile](https://clawhub.ai/user/blueworldmarketing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [Shell scripts and operational log or notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs persistent scheduled jobs and writes daily logs under the user's OpenClaw environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
