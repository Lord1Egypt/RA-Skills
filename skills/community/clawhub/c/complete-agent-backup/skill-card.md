## Description: <br>
A shell-script based backup and restore skill for Hermes Agent and OpenClaw agent state, including configuration, memories, skills, sessions, credentials, and workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoffguides](https://clawhub.ai/user/geoffguides) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure, create, and restore local backups for Hermes Agent or OpenClaw installations. It is intended for environments where operators can manage sensitive archives that may contain credentials, sessions, memories, and agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain API keys, bot tokens, credentials, sessions, memories, skills, and other sensitive agent state. <br>
Mitigation: Use encryption before cloud upload, keep archive permissions restricted, store encryption passwords in a password manager, and avoid sharing or committing backup files. <br>
Risk: Restore operations can overwrite an existing Hermes Agent or OpenClaw installation. <br>
Mitigation: Dry-run restores first, restore only archives from trusted sources, keep the automatic pre-restore backup until validation is complete, and avoid --force unless necessary. <br>
Risk: The security review flags restore-time safety gaps, including archive validation and decrypted temporary-file cleanup. <br>
Mitigation: Treat restored archives as sensitive, verify archive contents before applying them, and prefer manual review of backup files when restoring high-value or production agent state. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/geoffguides/complete-agent-backup) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke bundled shell scripts that create, encrypt, prune, or restore local backup archives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
