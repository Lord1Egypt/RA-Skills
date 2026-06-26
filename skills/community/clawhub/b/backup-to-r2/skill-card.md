## Description: <br>
Set up and run complete, encrypted, off-site backups of an OpenClaw install to Cloudflare R2 via restic, plus portable restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[servicosmkt](https://clawhub.ai/user/servicosmkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to protect, restore, or migrate OpenClaw configuration, agents, credentials, workspace, and scheduled jobs with encrypted off-site backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup includes OpenClaw credentials and auth profiles and uploads encrypted data to the user's private Cloudflare R2 bucket. <br>
Mitigation: Use a strong restic password, keep the R2 bucket private, verify RESTIC_REPOSITORY points to the intended bucket, and keep .restic-pass separate and private. <br>
Risk: Losing .restic-pass makes encrypted backups unrecoverable. <br>
Mitigation: Store the restic password safely outside the backup folder before relying on the backup workflow. <br>
Risk: The portable restore folder can contain both R2 credentials and the decryption key. <br>
Mitigation: Do not share the portable restore folder and remove copied credentials when restore work is complete. <br>
Risk: A real restore overwrites the active .openclaw installation with the latest backup. <br>
Mitigation: Run test-restore.ps1 first, inspect the restored backup, and proceed with restore-portable.ps1 only after explicit user confirmation. <br>
Risk: Non-destructive restore testing can leave decrypted OpenClaw data in a local restore-test folder. <br>
Mitigation: Inspect the test output locally and delete the restore-test folder after validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/servicosmkt/backup-to-r2) <br>
- [Publisher profile](https://clawhub.ai/user/servicosmkt) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [restic](https://restic.net) <br>
- [Cloudflare R2](https://developers.cloudflare.com/r2/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides backup setup, backup execution, non-destructive restore testing, scheduled backups, and portable restore.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
