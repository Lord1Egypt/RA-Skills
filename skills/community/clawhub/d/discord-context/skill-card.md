## Description:

Sync and cache per-thread context for Discord Forum channels. Use when handling /discord-context commands to poll active threads, list cached context, inspect a thread cache, or link a thread to a memory QMD file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demitrim](https://clawhub.ai/user/demitrim)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to poll active Discord Forum threads, cache per-thread context, inspect cached thread context, and link threads to local memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Discord bot token to poll forum threads.

Mitigation: Use an environment variable for DISCORD_TOKEN, avoid hardcoding secrets, and grant the bot only the server and channel permissions needed for this workflow.

Risk: The skill reads and writes cached context under the configured OpenClaw workspace memory tree.

Mitigation: Run it only against the intended workspace and review cached context before sharing or reusing it outside that workspace.

## Reference(s):

- [Discord Developer Portal](https://discord.com/developers/applications)
- [ClawHub Skill Page](https://clawhub.ai/demitrim/skills/discord-context)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Command-line text and optional JSON, with Markdown guidance for setup and use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and DISCORD_TOKEN for polling; reads and writes Discord cache files under the configured OpenClaw workspace memory tree.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
