## Description: <br>
Secure sync for OpenClaw memory and workspace with commands to push, restore, list, and check versioned backups for disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arakichanxd](https://clawhub.ai/user/arakichanxd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Claw Sync to back up and restore memory, profile, workspace rules, daily logs, and custom skills through a private Git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include sensitive OpenClaw memory, profile files, workspace rules, daily logs, and custom skills. <br>
Mitigation: Use a private, empty backup repository with a fine-grained token limited to that repository, inspect dry-run output, and review backup contents before relying on them. <br>
Risk: Restore operations can overwrite local files and restore executable custom skills, especially when force mode skips confirmation. <br>
Mitigation: Avoid force restores unless necessary, review backups before restoring skills, and keep the local backup created before restore available for rollback. <br>
Risk: Recurring auto-sync can upload workspace data every 12 hours. <br>
Mitigation: Enable auto-sync only when recurring uploads are intentional, and periodically audit the backup repository and token permissions. <br>


## Reference(s): <br>
- [Claw Sync on ClawHub](https://clawhub.ai/arakichanxd/claw-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text command output, setup guidance, and filesystem changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create versioned Git backups, local restore backups, restored workspace files, and optional recurring sync configuration.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
