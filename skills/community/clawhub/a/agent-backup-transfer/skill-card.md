## Description: <br>
Backup and restore an OpenClaw agent workspace and configuration so memory, identity, settings, and agent files can be preserved or moved to another computer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pacifier00](https://clawhub.ai/user/Pacifier00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, list, rotate, and restore portable backups of an OpenClaw workspace and configuration. It also supports migration workflows when moving an agent to another Linux or WSL2 computer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain sensitive OpenClaw identity, memory, configuration, session, or agent data. <br>
Mitigation: Keep archives private, encrypt them before transfer or upload, and avoid unencrypted sharing channels. <br>
Risk: Restoring an archive can overwrite existing OpenClaw files. <br>
Mitigation: Create a current backup first and inspect or extract the archive into a temporary directory before restoring. <br>
Risk: Restoring an untrusted archive could import unwanted or unsafe agent state. <br>
Mitigation: Restore only archives created by the user or from a trusted source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Pacifier00/agent-backup-transfer) <br>
- [Publisher profile](https://clawhub.ai/user/Pacifier00) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup, restore, listing, and hook setup instructions for OpenClaw files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
