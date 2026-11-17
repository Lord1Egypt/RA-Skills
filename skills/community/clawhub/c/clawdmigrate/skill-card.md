## Description:

Migrate moltbot or clawdbot assets to openclaw by discovering, backing up, copying, verifying files, and optionally running openclaw setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calabiyauman](https://clawhub.ai/user/calabiyauman)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to move local moltbot or clawdbot workspaces into the openclaw layout while preserving memory, configuration, clawdbook credentials, and project files. It is intended for migration workflows where users can review backups and verification results before continuing with openclaw onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may copy credentials, API keys, and other sensitive local files as part of migration.

Mitigation: Run it first on a copied workspace, inspect discovered files and backups, and avoid shared output or backup directories.

Risk: The openclaw setup path can perform a global npm install and run onboarding commands.

Mitigation: Review the package before execution and prefer pinned versions or manual openclaw installation/onboarding when global install behavior is not acceptable.

Risk: Migration behavior can be affected by symlinks or unexpected local filesystem layouts.

Mitigation: Inspect source directories for symlinks and unusual paths before running migration, especially when credentials are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calabiyauman/skills/clawdmigrate)
- [ClawHub publisher profile](https://clawhub.ai/user/calabiyauman)
- [README](README.md)
- [How to run](HOW_TO_RUN.md)
- [Migration sources](Documentation/MIGRATION_SOURCES.md)
- [Openclaw setup](Documentation/OPENCLAW_SETUP.md)
- [Post-migration verification](Documentation/VERIFICATION.md)
- [npm package page](https://www.npmjs.com/package/clawd-migrate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with JSON summaries and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or copy local files during migration, produce backups and verification reports, and invoke npm/openclaw setup commands when selected or enabled.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata; artifact package files report 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
