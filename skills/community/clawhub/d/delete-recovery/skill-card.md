## Description: <br>
Automatically backs up files before deletion, restores deleted files, lists and searches backups, verifies backup integrity, and cleans expired backups and logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce accidental file-deletion loss by creating recoverable backups before deletion, restoring deleted files, searching backup records, and managing opt-in workspace cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has deletion and cleanup capabilities that can remove workspace files when invoked. <br>
Mitigation: Use the workspace cleaner dry-run and token confirmation flow before enabling cleanup, review the previewed file list, and keep important paths whitelisted. <br>
Risk: Backups and logs remain in .delete_recovery after skill use and may contain recoverable copies or operational records. <br>
Mitigation: Clean expired backups and logs when retention is no longer needed, and treat .delete_recovery as workspace data requiring normal access controls. <br>
Risk: Disabling workspace confinement with empty allowed_roots can restore files outside the workspace. <br>
Mitigation: Keep the default workspace-root confinement unless a deliberate legacy restore requires broader access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cloudcode-hans/delete-recovery) <br>
- [Publisher Profile](https://clawhub.ai/user/cloudcode-hans) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates workspace-local backup, manifest, configuration, and log files under .delete_recovery.] <br>

## Skill Version(s): <br>
0.11.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
