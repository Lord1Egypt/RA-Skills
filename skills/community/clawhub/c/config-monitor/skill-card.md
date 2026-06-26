## Description: <br>
Monitors OpenClaw Gateway status, configuration change frequency, backup health, related skill availability, and log errors, then produces configuration health reports and alert-response guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samlinfj](https://clawhub.ai/user/samlinfj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw configuration health, review Gateway status and backup readiness, and respond to configuration-related alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational monitoring guidance includes shell commands that inspect logs, restart Gateway services, roll back configuration, and clean old backup files. <br>
Mitigation: Review each command before execution, preview backup files before cleanup, and keep extra recovery copies when backups matter. <br>


## Reference(s): <br>
- [Config Monitor on ClawHub](https://clawhub.ai/samlinfj/config-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and monitoring report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trigger phrases, command sequences, alert workflows, and scheduled monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
