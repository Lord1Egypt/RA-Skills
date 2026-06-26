## Description: <br>
Complete toolkit for creating autonomous AI agents and managing Discord channels for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create OpenClaw agent workspaces, bind agents to Discord channels, manage channel setup or renaming, and configure gateway allowlists for multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Discord and OpenClaw configuration changes. <br>
Mitigation: Inspect generated gateway patches, use a Discord bot with minimal permissions, and confirm the target guild, channel IDs, workspace path, and agent ID before running scripts. <br>
Risk: The skill can create persistent agent automation through gateway bindings, workspaces, and cron jobs. <br>
Mitigation: Review and remove created gateway bindings, agent workspaces, and cron jobs when they are no longer needed. <br>
Risk: Workspace rename operations can modify Markdown files under the selected workspace. <br>
Mitigation: Avoid broad workspace paths and review changed files before committing or relying on the renamed references. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw agents documentation](https://docs.openclaw.ai/agents) <br>
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration patches, and generated Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can create local agent workspaces, Discord channels, OpenClaw gateway bindings, and optional cron jobs when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
