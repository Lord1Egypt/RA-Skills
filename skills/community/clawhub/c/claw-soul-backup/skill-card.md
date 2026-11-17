## Description:

Stores encrypted OpenClaw workspace backups and supports restore workflows through Claw Vault with local encryption and token-secured API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielglh](https://clawhub.ai/user/danielglh)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to create encrypted workspace backup archives, upload them to Claw Vault, schedule daily replacement backups, and manage token-secured backup credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled backups can upload encrypted workspace archives to Claw Vault without enough visibility into file scope, encryption, destination, credential storage, cron entries, or logs.

Mitigation: Confirm the archive contents, encryption method, destination, credential storage location, cron entry, log path, disable procedure, and credential rotation plan before enabling automation.

Risk: The artifact directs agents to follow mutable remote instructions for current response formats and the API contract.

Mitigation: Review the remote instructions separately before treating them as permission for new agent behavior, and prefer pinned, locally reviewed instructions for deployment.

Risk: The backup ID and API token authorize sensitive backup operations.

Mitigation: Treat backup IDs and API tokens as secrets, store them only in a user-approved secure location, never print them in logs or chat output, and rotate them if exposed.

## Reference(s):

- [Claw Soul Backup release page](https://clawhub.ai/danielglh/skills/claw-soul-backup)
- [Claw Vault homepage](https://www.claw-vault.com)
- [Claw Vault canonical instructions and API details](https://www.claw-vault.com/SKILL.md)
- [Claw Vault API host](https://api.claw-vault.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl and cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local scripts, encrypted archive handling, credential storage steps, and cron scheduling.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
