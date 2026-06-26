## Description: <br>
Back up the full OpenClaw environment (~/.openclaw) to a Git repository. Supports scheduled backups, interactive restore, and Git LFS for large model files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to back up OpenClaw state to a trusted Git repository, schedule recurring backups, and restore prior backup commits when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can copy highly sensitive OpenClaw data, including credentials, identity keys, knowledge bases, and agent memory, into a Git repository. <br>
Mitigation: Use only a trusted private repository, review the generated .gitignore and repository contents before pushing, and treat backup repositories as secret-bearing data. <br>
Risk: The skill requires a Git token and stores or passes credentials for backup and scheduled push operations. <br>
Mitigation: Use a minimally scoped, revocable token, rotate it when access changes, and remove scheduled jobs before decommissioning the backup. <br>
Risk: Untrusted repository URLs or cron expressions can affect shell-based Git and scheduling behavior. <br>
Mitigation: Configure only trusted repository URLs and cron expressions, then inspect the installed crontab after enabling or changing scheduled backups. <br>
Risk: Restore operations overwrite the current OpenClaw directory from a selected backup commit. <br>
Mitigation: Restore only from trusted backup history and confirm the selected commit before allowing the restore to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixsonwang/claw-saver) <br>
- [Publisher profile](https://clawhub.ai/user/jixsonwang) <br>
- [Skill homepage from artifact metadata](https://clawhub.ai/skills/claw-saver) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Markdown, Guidance] <br>
**Output Format:** [CLI text output, JSON configuration, Git commits, and generated RESTORE.md guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, git-lfs, skills/claw-saver/config.json, and OPENCLAW_BACKUP_GIT_TOKEN; backup data may include sensitive OpenClaw state.] <br>

## Skill Version(s): <br>
1.6.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
