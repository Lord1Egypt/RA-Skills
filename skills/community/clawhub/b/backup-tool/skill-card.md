## Description: <br>
Backup and restore files with compression and encryption. Use when user needs to backup important files, create scheduled backups, sync folders, encrypt sensitive backups, or restore from backup archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to create, list, and restore compressed tar backups from local paths, including scheduled backup command examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local files during restore operations. <br>
Mitigation: Review restore destinations before execution and restore only archives from trusted sources. <br>
Risk: The advertised encryption, incremental backup, and exclude features do not match the implementation. <br>
Mitigation: Do not rely on those features until the implementation is fixed and verified. <br>
Risk: Broad scheduled backup paths can capture more local data than intended. <br>
Mitigation: Review cron entries and backup paths before scheduling automated runs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local archive files when the generated commands are executed by an agent or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
