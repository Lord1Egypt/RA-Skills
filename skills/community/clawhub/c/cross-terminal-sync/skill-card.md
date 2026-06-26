## Description: <br>
Cross Terminal Sync helps WorkBuddy users continue work across Mac and Windows by combining OneDrive file synchronization with optional OneDrive MCP search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenyang-x](https://clawhub.ai/user/zenyang-x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to initialize, check, and troubleshoot cross-device task handoff between Mac and Windows systems. It provides guidance, configuration snippets, and shell commands for syncing selected WorkBuddy state through OneDrive and optionally searching OneDrive through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to move or link sensitive WorkBuddy identity, memory, profile, and database files into OneDrive. <br>
Mitigation: Review exactly which files will be synced before setup, keep local backups, and avoid syncing identity, profile, or database files unless that state is needed across devices. <br>
Risk: Persistent symlinks, junctions, or scheduled copy jobs can overwrite or expose local agent state if configured incorrectly. <br>
Mitigation: Validate link targets before running setup commands, preserve backups of existing files, and inspect sync status before reading or writing cross-device state. <br>
Risk: The optional OneDrive MCP server receives OAuth read/write access to OneDrive. <br>
Mitigation: Treat the MCP server as a separate third-party component, install it only when intentional, and review its permissions and credential storage before use. <br>


## Reference(s): <br>
- [Cross Terminal Sync ClawHub page](https://clawhub.ai/zenyang-x/cross-terminal-sync) <br>
- [onedrive-mcp-server repository](https://github.com/MrFixit96/onedrive-mcp-server.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, PowerShell, CMD, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose filesystem links, OneDrive sync checks, MCP setup, and backup or fallback procedures for user review before execution.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
