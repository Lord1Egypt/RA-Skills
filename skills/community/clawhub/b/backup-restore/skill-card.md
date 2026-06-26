## Description: <br>
Creates full and incremental OpenClaw backups, verifies backup archives, and provides backup-management commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhui435](https://clawhub.ai/user/yuhui435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to generate backup archives for OpenClaw configuration, workspace data, skills, and agent workspaces, then list or verify those archives before storage or recovery planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill overstates recovery capability and the restore command can report success without restoring data. <br>
Mitigation: Treat generated backups as unproven for disaster recovery until restore behavior is implemented, tested, and verified in the target environment. <br>
Risk: Generated backup archives may contain private workspace and configuration data. <br>
Mitigation: Store backup archives in protected locations with appropriate access controls and retention handling. <br>
Risk: The backup path must match the user's actual OpenClaw directory. <br>
Mitigation: Review and update the configured backup path before relying on the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuhui435/backup-restore) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, files] <br>
**Output Format:** [Python command output, JSON cron configuration, and ZIP backup archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backup archives may contain private configuration and workspace data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
