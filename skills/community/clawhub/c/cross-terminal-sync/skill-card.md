## Description:

Cross Terminal Sync helps WorkBuddy agents continue work across Mac and Windows terminals using OneDrive file synchronization with optional MCP-based cloud search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenyang-x](https://clawhub.ai/user/zenyang-x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to configure cross-terminal continuity between Mac and Windows, search prior work across terminals, and resume tasks through OneDrive local sync or an optional OneDrive MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill syncs WorkBuddy memory, identity/profile files, skills, projects, and automation data through OneDrive, which may expose sensitive agent context to every device or cloud principal with access.

Mitigation: Use a dedicated OneDrive sync folder with least-privilege access, avoid syncing agent control files unless all synced devices and cloud accounts are trusted, and document how to revoke OAuth access.

Risk: The optional OneDrive MCP server uses broad file read/write access and can search, download, upload, and create sharing links for cloud files.

Mitigation: Install only a pinned and reviewed MCP server version, restrict its scope where possible, and review requested OneDrive permissions before enabling it.

Risk: Hourly fallback automation and cross-device file links can propagate stale or unintended WorkBuddy state between terminals.

Mitigation: Verify sync status before reading cross-terminal files, preserve backups before creating links or junctions, and keep a documented disable path for scheduled synchronization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zenyang-x/skills/cross-terminal-sync)
- [onedrive-mcp-server](https://github.com/MrFixit96/onedrive-mcp-server.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash, PowerShell, CMD, JSON, and pseudocode blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific OneDrive path checks, sync validation steps, fallback options, and conflict-prevention guidance.]

## Skill Version(s):

2.2.0 (source: frontmatter, ClawHub release metadata, _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
