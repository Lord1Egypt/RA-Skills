## Description: <br>
clawd-migrate helps migrate moltbot or clawdbot assets to openclaw by discovering, backing up, copying, verifying, and optionally setting up the migrated workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calabiyauman](https://clawhub.ai/user/calabiyauman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when moving existing moltbot or clawdbot workspaces into the openclaw layout while preserving memory, configuration, clawdbook data, and project files. It is intended for migration planning and execution where backups and post-copy verification are part of the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration can copy credentials, API keys, memory, and instruction files into backups and OpenClaw configuration folders. <br>
Mitigation: Run only against an explicit trusted source directory, keep backup and output folders private, and review migrated credential and instruction files before use. <br>
Risk: The default migration flow can globally reinstall OpenClaw and run onboarding after migration. <br>
Mitigation: Use an isolated environment or review and adjust the workflow before allowing global installation or onboarding commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calabiyauman/clawdmigrate) <br>
- [README](artifact/README.md) <br>
- [How to run](artifact/HOW_TO_RUN.md) <br>
- [Migration sources](artifact/Documentation/MIGRATION_SOURCES.md) <br>
- [Post-migration verification](artifact/Documentation/VERIFICATION.md) <br>
- [OpenClaw setup](artifact/Documentation/OPENCLAW_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, plus terminal output and JSON-style migration or verification status when commands run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backup directories, migrated openclaw folders, and verification reports as part of migration execution.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
