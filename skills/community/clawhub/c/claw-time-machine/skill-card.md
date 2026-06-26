## Description: <br>
Backup, restore, and migrate OpenClaw installations while preserving workspace memories, credentials, custom skills, scheduled tasks, and core configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tacitlab](https://clawhub.ai/user/tacitlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up, restore, inspect, and migrate OpenClaw state across local or remote installations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain sensitive OpenClaw state, including credentials and identity files. <br>
Mitigation: Review backup contents when appropriate, keep archives private, and restrict access to ~/.ctm/ and copied migration archives. <br>
Risk: Restore and migrate operations overwrite preserved OpenClaw state paths. <br>
Mitigation: List and confirm the selected backup first, preserve the script's safety backup path, and use --force only when non-interactive overwrite is intended. <br>
Risk: Migration copies a backup archive to a remote host and restores it over SSH. <br>
Mitigation: Verify the target host and remote directory before migration, and use --clean-remote-archive when the copied archive should not remain on the target machine. <br>


## Reference(s): <br>
- [Usage Notes](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tacitlab/claw-time-machine) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates tar.gz backups under ~/.ctm/ and can restore or migrate OpenClaw state when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
