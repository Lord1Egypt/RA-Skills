## Description: <br>
Complete Discord integration for Clawdbot with automatic UI installation, setup wizard, credential management, server monitoring, dashboard controls, and plugin architecture hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to add Discord as a Clawdbot channel, including dashboard setup, token configuration, server monitoring, Discord RPC methods, and health diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can patch Clawdbot source files, rebuild the project, and restart the gateway. <br>
Mitigation: Review installer changes first, run with --dry-run, use --skip-build and --skip-restart until ready, and keep a backup of the Clawdbot source tree. <br>
Risk: Uninstall may not fully restore all source modifications. <br>
Mitigation: Record installed files and patches before installation, keep backups, and plan for manual cleanup or restore from version control. <br>
Risk: Discord bot tokens grant API access and may expose guild, channel, and message capabilities according to assigned permissions. <br>
Mitigation: Use a dedicated least-privilege bot token, store it with OpenBao or environment-based secret handling, avoid committing tokens, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/discord-connect-ui) <br>
- [Publisher profile](https://clawhub.ai/user/maverick-software) <br>
- [Discord Bot Setup Guide](references/bot-setup.md) <br>
- [Discord Connect Troubleshooting Guide](references/troubleshooting.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Bot Permissions Calculator](https://discordapi.com/permissions.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration examples, TypeScript assets, JavaScript installers, Python diagnostics, and JSON schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and troubleshooting guidance plus bundled files for Discord UI, RPC handlers, token checks, health checks, and configuration validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
