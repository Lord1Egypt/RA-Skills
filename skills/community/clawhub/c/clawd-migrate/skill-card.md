## Description: <br>
Migrates moltbot or clawdbot data to openclaw by backing up, transferring config, memory, and clawdbook data with verification and setup support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calabiyauman](https://clawhub.ai/user/calabiyauman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to migrate existing moltbot or clawdbot workspaces into the openclaw layout while preserving memory, configuration, clawdbook credentials, and project files. It is intended for local migration workflows that need discovery, backup, copy, verification, and optional openclaw setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration may copy credential-bearing configuration, clawdbook, or API key files into backups and destination folders. <br>
Mitigation: Run it in a controlled account, review backup and destination permissions, and avoid shared or repository-backed output folders. <br>
Risk: The workflow may globally reinstall openclaw and run onboarding commands as part of migration or setup. <br>
Mitigation: Prefer dry-run discovery or manual migration first, and only allow install or onboarding steps when they are explicit and intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/calabiyauman/clawd-migrate) <br>
- [README](artifact/README.md) <br>
- [How to Run](artifact/HOW_TO_RUN.md) <br>
- [Migration Sources](artifact/Documentation/MIGRATION_SOURCES.md) <br>
- [Post-Migration Verification](artifact/Documentation/VERIFICATION.md) <br>
- [Openclaw Setup](artifact/Documentation/OPENCLAW_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and migration status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct file backup, migration, verification, and openclaw setup actions when executed by an agent or user.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
