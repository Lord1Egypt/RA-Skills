## Description:

Provides Discord bot connectivity for Clawdbot with automatic dashboard tab installation, setup, credential management, server monitoring, RPC handlers, and plugin hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add and manage a Discord channel in Clawdbot, including bot setup, token configuration, health checks, server and channel views, and dashboard controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify and restart a Clawdbot installation.

Mitigation: Review before installing, run in a test Clawdbot checkout first, use dry-run and skip-restart options where possible, and back up the gateway/UI source tree.

Risk: Discord bot tokens may be handled in ways that are not fully safe, especially when passed on the command line.

Mitigation: Avoid passing live Discord tokens on the command line, prefer a real secret manager such as OpenBao, and rotate tokens if exposure is suspected.

Risk: Discord bot permissions can grant broader access than needed.

Mitigation: Grant the bot minimal Discord permissions and verify guild and channel permissions before normal use.

Risk: Uninstalling may require manual cleanup of modified Clawdbot files.

Mitigation: Be prepared for manual cleanup and verify backend, UI, and navigation files after uninstalling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/discord-connect-ui)
- [Discord Bot Setup Guide](references/bot-setup.md)
- [Discord Connect Troubleshooting Guide](references/troubleshooting.md)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.js Documentation](https://discord.js.org/)
- [Bot Permissions Calculator](https://discordapi.com/permissions.html)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands, TypeScript/JavaScript/Python code assets, and JSON configuration schema.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install and health-check scripts, UI/backend assets, and references for Discord setup and troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
