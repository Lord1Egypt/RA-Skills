## Description: <br>
Backup and restore ClawdBot configuration, skills, commands, and settings. Sync across devices, version control with git, automate backups, and migrate to new machines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sebastian-Buitrag0](https://clawhub.ai/user/Sebastian-Buitrag0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ClawdBot users use this skill to create, verify, restore, sync, and automate backups of local ClawdBot configuration, skills, commands, settings, and MCP configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives, git repositories, and cloud sync targets may contain private ClawdBot configuration. <br>
Mitigation: Keep archives and remotes private, review ~/.claude contents before syncing or pushing, and exclude credentials or machine-specific files where appropriate. <br>
Risk: Restore commands and rsync --delete workflows can overwrite or remove local configuration. <br>
Mitigation: Make a current backup first, preview archive contents or sync paths before applying changes, and confirm the target directory before restoring. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sebastian-Buitrag0/clawdbot-backup) <br>
- [Publisher profile](https://clawhub.ai/user/Sebastian-Buitrag0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, tar, and rsync for the documented backup, restore, sync, and version-control workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
