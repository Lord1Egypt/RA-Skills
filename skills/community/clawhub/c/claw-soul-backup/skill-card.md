## Description: <br>
Store encrypted OpenClaw workspace backups and restore them through Claw Vault using local encryption and token-secured API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielglh](https://clawhub.ai/user/danielglh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create encrypted backups of OpenClaw workspaces, upload them to Claw Vault, and configure recurring daily updates after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to consult mutable remote instructions that can change after review. <br>
Mitigation: Verify the current remote instructions before use and stop if they conflict with user policy or local requirements. <br>
Risk: Workspace archives can contain sensitive files or secrets. <br>
Mitigation: Encrypt archives locally, limit what goes into each archive, and never upload raw workspace files. <br>
Risk: Backup IDs and API tokens can authorize backup updates or access. <br>
Mitigation: Treat backup IDs and API tokens as secrets, store them only in a user-approved secure location, and avoid printing them in logs or chat. <br>
Risk: A recurring cron job can keep uploading backups after the initial setup. <br>
Mitigation: Create scheduled backups only with explicit user approval and document how to disable the job. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/danielglh/claw-soul-backup) <br>
- [Claw Vault homepage](https://www.claw-vault.com) <br>
- [Claw Vault canonical instructions](https://www.claw-vault.com/SKILL.md) <br>
- [Claw Vault API host](https://api.claw-vault.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoints and secret-handling guidance; users must supply encryption and storage choices.] <br>

## Skill Version(s): <br>
0.1.8 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
