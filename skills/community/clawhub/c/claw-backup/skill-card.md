## Description: <br>
Back up OpenClaw customizations (memory, config, skills, workspace) to cloud storage via rclone, with scheduling + retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vidarbrekke](https://clawhub.ai/user/vidarbrekke) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure scheduled backups of local OpenClaw memory, configuration, skills, workspace files, and related project data to a local archive or rclone destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include sensitive OpenClaw memory, configuration, skills, workspace files, and project data. <br>
Mitigation: Review the generated backup script, test local-only mode first, and use an encrypted rclone destination or encrypt archives before offsite storage. <br>
Risk: The setup can install recurring scheduler entries and retention rules that upload data or delete older backup archives. <br>
Mitigation: Confirm scheduler, upload mode, destination, and retention settings before enabling automation, then inspect the LaunchAgent, crontab, or Task Scheduler entry after installation. <br>
Risk: Executing install scripts directly from a one-line download gives the script immediate local access. <br>
Mitigation: Prefer the git clone installation path and inspect setup.js plus the scheduler installer before running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vidarbrekke/claw-backup) <br>
- [Publisher profile](https://clawhub.ai/user/vidarbrekke) <br>
- [ClawBackup repository](https://github.com/vidarbrekke/ClawBackup) <br>
- [rclone installation documentation](https://rclone.org/install/) <br>
- [Node.js downloads](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local backup scripts, scheduler entries, rclone destinations, and restore notes.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter and README state 1.0.15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
