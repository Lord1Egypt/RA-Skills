## Description: <br>
Create a full local backup of the OpenClaw workspace and configuration using the existing backup-local.sh script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trumppo](https://clawhub.ai/user/Trumppo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to ask an agent to run a local OpenClaw full-backup wrapper and report the resulting archive path and size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain workspace files, configuration, or secrets. <br>
Mitigation: Protect archives in /root/.openclaw/backups and restrict access to users who need local backup data. <br>
Risk: The wrapper delegates the actual backup operation to the external backup-local.sh script. <br>
Mitigation: Review backup-local.sh before deployment or execution to confirm backup scope, exclusions, and archive handling. <br>


## Reference(s): <br>
- [Fullbackup skill page](https://clawhub.ai/Trumppo/fullbackup) <br>
- [Trumppo publisher profile](https://clawhub.ai/user/Trumppo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text status output with archive path and size] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill invokes a local backup wrapper and keeps the resulting archive locally.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
