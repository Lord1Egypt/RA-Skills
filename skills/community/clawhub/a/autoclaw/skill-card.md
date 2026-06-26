## Description: <br>
Automates health monitoring, scheduled backups, and process logging for AI assistant workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shayuqiang671-rgb](https://clawhub.ai/user/shayuqiang671-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use AutoClaw to check key AI workspace files, create local backups, and log workspace health and process status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script uses a hardcoded workspace path and creates local backup and log files. <br>
Mitigation: Edit the workspace path before running and confirm that the configured workspace and backup directory are appropriate. <br>
Risk: Backup cleanup prunes older backup folders after the configured retention limit. <br>
Mitigation: Review the listed files and retention setting before scheduling the script or relying on its backups. <br>
Risk: Running the script from cron or Task Scheduler can repeatedly modify local backup and log directories. <br>
Mitigation: Run it manually first and schedule it only after confirming the local file changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shayuqiang671-rgb/autoclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime script writes timestamped console and file logs, creates local backup folders, and prunes older backups after the configured retention limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
