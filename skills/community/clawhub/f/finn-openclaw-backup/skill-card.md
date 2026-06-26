## Description: <br>
Backs up key OpenClaw configuration files into a timestamped folder on the user's Desktop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create a local backup of OpenClaw configuration, agent definitions, credentials, and cron files before maintenance, migration, or recovery work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated backup includes credentials and API keys. <br>
Mitigation: Store the backup in encrypted or access-restricted storage, avoid desktop sync or sharing, and delete old backups when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meowlegemy-sudo/finn-openclaw-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and local shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped local backup folder on the user's Desktop when the provided shell script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
