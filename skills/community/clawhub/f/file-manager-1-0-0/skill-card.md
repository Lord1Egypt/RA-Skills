## Description: <br>
OpenClaw file-management assistant for batch file operations, file organization, duplicate cleanup, renaming, directory synchronization, and related local file workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhenyoyo](https://clawhub.ai/user/yangzhenyoyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and end users can use this skill to have an agent plan and run local file organization, renaming, duplicate cleanup, and directory synchronization workflows. It is most useful when the user wants preview-first file-management commands with explicit confirmation before destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File-management commands can rename, move, delete, or synchronize local files. <br>
Mitigation: Start with preview, scan-only, or dry-run modes; test on explicit folders; and require user confirmation before executing changes. <br>
Risk: Duplicate cleanup and mirror synchronization can remove files if run with destructive options. <br>
Mitigation: Prefer quarantine or move actions over permanent deletion, keep backups, and review generated reports before using delete or mirror-delete behavior. <br>
Risk: Scheduled automation can repeatedly apply an incorrect file-management rule. <br>
Mitigation: Avoid cron or task-scheduler use until the command has been verified manually and dependencies are pinned in controlled environments. <br>


## Reference(s): <br>
- [File Management Best Practices](references/best_practices.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yangzhenyoyo/file-manager-1-0-0) <br>
- [Publisher Profile](https://clawhub.ai/user/yangzhenyoyo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that inspect, copy, move, rename, delete, or synchronize local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
