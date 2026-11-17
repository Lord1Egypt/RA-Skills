## Description:

Migrates moltbot or clawdbot data to openclaw by backing up and transferring config, memory, project, and clawdbook data with verification and optional OpenClaw setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calabiyauman](https://clawhub.ai/user/calabiyauman)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to migrate local moltbot or clawdbot workspaces into the openclaw layout while preserving memory files, configuration, clawdbook credentials, and project files. It supports discovery, backup, migration, verification, and post-migration setup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration reads and copies credential and configuration files.

Mitigation: Run it only on trusted source workspaces, protect generated backups, and inspect the migrated directory before using it.

Risk: OpenClaw setup may modify the user's global npm environment.

Mitigation: Review the setup step before execution and prefer an explicit, version-pinned OpenClaw install when operating in managed environments.

Risk: Untrusted source workspaces may contain symlinks or unexpected file layouts.

Mitigation: Inspect source directories before migration and avoid running the tool against workspaces from untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calabiyauman/skills/clawd-migrate)
- [README](artifact/README.md)
- [How to run](artifact/HOW_TO_RUN.md)
- [Migration sources](artifact/Documentation/MIGRATION_SOURCES.md)
- [Post-migration verification](artifact/Documentation/VERIFICATION.md)
- [OpenClaw setup after migration](artifact/Documentation/OPENCLAW_SETUP.md)
- [Platform support](artifact/Documentation/PLATFORMS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Terminal output, copied files, timestamped backups, and verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and copy credential/configuration files; migration can create backups and run OpenClaw setup commands after file verification.]

## Skill Version(s):

0.2.1 (source: server release evidence; artifact package metadata reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
