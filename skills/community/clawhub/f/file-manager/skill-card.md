## Description: <br>
File Manager helps agents organize, rename, deduplicate, and synchronize local files with preview-first Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and run local file management workflows, including folder organization, batch renaming, duplicate-file cleanup, and directory mirroring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File organization, rename, delete, and sync actions can change or remove local files. <br>
Mitigation: Run preview or scan-only modes first, confirm source and target paths, and keep backups before executing broad operations. <br>
Risk: Automated or scheduled runs can repeatedly apply an incorrect file-management rule. <br>
Mitigation: Test workflows on a non-critical folder before scheduling them and review exclusions, delete flags, and destination paths. <br>


## Reference(s): <br>
- [File management best practices](references/best_practices.md) <br>
- [ClawHub skill page](https://clawhub.ai/russellfei/file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first workflows; file changes require explicit command execution and confirmation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
