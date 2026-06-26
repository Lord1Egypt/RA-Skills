## Description: <br>
Comprehensive backup, update, and restore workflow with dynamic workspace detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to maintain Clawdbot installations by previewing backups, creating full backups, checking upstream updates, validating setup, and restoring state if an update fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain credentials, session data, and workspace contents. <br>
Mitigation: Keep ~/.clawdbot-backups private with restrictive permissions or encryption, and do not share backup archives. <br>
Risk: Backup and restore scripts have broad local access to Clawdbot configuration, state, and workspaces. <br>
Mitigation: Run the dry-run script first and review workspace paths in ~/.clawdbot/clawdbot.json before creating or restoring a backup. <br>
Risk: Restoring from an untrusted or incorrect backup can overwrite current configuration and workspaces. <br>
Mitigation: Restore only from backups you trust and verify the backup directory before confirming the restore workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pasogott/clawdbot-skill-update) <br>
- [Publisher profile](https://clawhub.ai/user/pasogott) <br>
- [Skill homepage](https://github.com/pasogott/clawdbot-skill-update) <br>
- [Clawdbot repository](https://github.com/clawdbot/clawdbot) <br>
- [README](artifact/README.md) <br>
- [Quick Reference](artifact/QUICK_REFERENCE.md) <br>
- [Update Checklist](artifact/UPDATE_CHECKLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and executable shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup archives and restore actions when the bundled shell scripts are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact package.json and config.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
