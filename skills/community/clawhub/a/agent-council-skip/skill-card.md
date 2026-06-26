## Description: <br>
Complete toolkit for creating autonomous AI agents and managing Discord channels for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[izletenadam-creator](https://clawhub.ai/user/izletenadam-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create OpenClaw agents with workspaces, memory files, gateway configuration, optional Discord bindings, and optional daily memory cron jobs. They also use it to create or rename Discord channels and produce the OpenClaw configuration commands needed to connect those channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw gateway, workspace, Discord, and cron changes. <br>
Mitigation: Review every generated command before execution, use fresh workspaces, and remove or adjust gateway patches and cron jobs that are no longer needed. <br>
Risk: Discord channel creation and rename actions can affect shared server organization. <br>
Mitigation: Confirm channel IDs, category IDs, bot permissions, and rename targets before applying changes. <br>
Risk: Agent memory and Discord channels may capture sensitive personal or health data. <br>
Mitigation: Avoid sensitive data unless appropriate access controls, retention practices, and user consent are in place. <br>
Risk: Workspace rename operations can modify Markdown files across a workspace. <br>
Mitigation: Run from a clean workspace, inspect reported file changes, and review diffs before committing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/izletenadam-creator/agent-council-skip) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw agents documentation](https://docs.openclaw.ai/agents) <br>
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration patches, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent OpenClaw gateway changes, Discord channel changes, workspace Markdown files, and optional cron jobs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
