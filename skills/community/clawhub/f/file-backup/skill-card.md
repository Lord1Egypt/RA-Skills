## Description: <br>
File Backup guides an agent to create a local backup before editing important files, ask the user to review the result, and delete the backup only after explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jiaqi-Guo-0114](https://clawhub.ai/user/Jiaqi-Guo-0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve copies of important local files before changes, review the edited files, and clean up backups only after they confirm the result is correct. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain the same sensitive data as the original files. <br>
Mitigation: Use a trusted backup directory and delete backups after the user verifies that the edited files are correct. <br>
Risk: Incorrect backup or deletion paths could preserve the wrong file or remove a backup before review. <br>
Mitigation: Show the backup path to the user and require explicit confirmation before deleting the backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jiaqi-Guo-0114/file-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup path reminders and confirmation-gated cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
