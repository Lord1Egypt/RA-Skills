## Description: <br>
Manages synchronization guidance for shared dotfiles, agent configurations, MCP server settings, Serena memory, and Syncthing diagnostics across developer tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage shared AI-tool configuration, dotfile templates, MCP server lists, session knowledge sync, and Syncthing setup or troubleshooting across local machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap and sync steps can reshape existing Claude, Codex, Gemini, Antigravity, and shared agent configuration directories. <br>
Mitigation: Inspect the scripts first, back up existing ~/.claude, ~/.codex, ~/.gemini, ~/.agents, Syncthing, and Serena data, and verify symlink targets before relying on the result. <br>
Risk: Knowledge sync can persist session-derived project information into Serena memory. <br>
Mitigation: Review candidate memories before writing them and exclude secrets, credentials, and sensitive infrastructure details. <br>
Risk: Syncthing setup and diagnostic commands can change folder configuration or expose local API keys and passwords in shared logs or shell history. <br>
Mitigation: Use real API keys only locally, avoid pasting credentials into logs or tickets, and review .stignore and folder settings before applying changes. <br>


## Reference(s): <br>
- [Dotfile on ClawHub](https://clawhub.ai/drumrobot/dotfile) <br>
- [Multi-Agent Shared Layout](agents.md) <br>
- [chezmoi Template Management](chezmoi.md) <br>
- [Knowledge Sync](knowledge.md) <br>
- [MCP Server Synchronization](mcp.md) <br>
- [Syncthing Integration](syncthing.md) <br>
- [Release Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to inspect, back up, symlink, or update local configuration files before applying changes.] <br>

## Skill Version(s): <br>
0.4.1 (source: evidence.release.version and CHANGELOG, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
