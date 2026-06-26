## Description: <br>
Automatically backs up OpenClaw agent state files daily via cron into compressed archives and supports manual restore for migration or recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benxiao2026](https://clawhub.ai/user/benxiao2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to back up identity, personality, memory, user, and knowledge-base files and restore them during migration or recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain sensitive identity, memory, user, and knowledge-base data. <br>
Mitigation: Store archives in a protected location, restrict access, and treat copied backup files as sensitive data. <br>
Risk: Restore operations can overwrite the current OpenClaw state. <br>
Mitigation: Create or verify a current backup before restoring, and restore only from archives you trust. <br>
Risk: Retention cleanup deletes older backup archives. <br>
Mitigation: Review the retention command and adjust the archive count before enabling automated cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benxiao2026/agent-state-backup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local backup, restore, cron setup, retention, and log inspection steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
