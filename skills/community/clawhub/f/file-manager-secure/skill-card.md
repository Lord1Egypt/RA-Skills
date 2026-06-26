## Description: <br>
Perform safe file operations with path validation, dry-run previews, recoverable trash deletes, batch confirmations, and audit logging to prevent data loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houssameddinemaatallah](https://clawhub.ai/user/houssameddinemaatallah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage files inside a configured workspace, including listing, searching, copying, moving, deleting to trash, and restoring files. It is intended for workflows that need previews, audit logs, and recoverable operations before changing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore and delete-confirm paths can move or write files without rechecking the workspace boundary. <br>
Mitigation: Keep OPENCLAW_WORKSPACE narrow, review generated operation JSON before delete-confirm, and restore only from trash metadata that was created by a trusted run. <br>
Risk: The skill can change or remove local files when execution commands are confirmed. <br>
Mitigation: Run dry-run planning first, inspect file lists and destinations, and use backups or trash recovery before applying bulk operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houssameddinemaatallah/file-manager-secure) <br>
- [Publisher profile](https://clawhub.ai/user/houssameddinemaatallah) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [File manager script](artifact/scripts/file_manager.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown instructions and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations are scoped to OPENCLAW_WORKSPACE and may create trash, backup, and audit-log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
