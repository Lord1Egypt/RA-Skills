## Description: <br>
专业的文件夹整理助手，帮助用户安全地整理和清理文件夹，在清理前自动创建压缩备份，使用移动命令代替删除命令确保数据安全，并支持需在桌面端使用的 Mac/Linux 和 Windows 系统。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to safely analyze, organize, and clean selected local folders with backups, confirmation steps, and recovery reporting. It is intended for desktop environments where the agent can access the user-selected filesystem path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and move files in folders selected by the user. <br>
Mitigation: Confirm the exact target folder and review the proposed file list before allowing cleanup actions. <br>
Risk: Moved files and backup archives may retain sensitive data. <br>
Mitigation: Verify the backup destination, protect the backup archive, and remove retained copies when they are no longer needed. <br>
Risk: Filesystem changes may be difficult to review after execution. <br>
Mitigation: Require a backup before cleanup and provide a report with moved file counts, trash location, and restoration instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/folder-cleanup-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash or PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes folder analysis, proposed cleanup actions, backup location, moved-file report, trash location, and recovery guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
