## Description: <br>
Complete toolkit for creating autonomous AI agents and managing Discord channels for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up OpenClaw multi-agent systems, create autonomous agents with isolated workspaces and memory files, and manage Discord channel bindings and organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references shell and Python scripts for OpenClaw, Discord, workspace, and cron changes that were not included in the evidence bundle for review. <br>
Mitigation: Obtain the referenced scripts from a trusted source and inspect them before running any command. <br>
Risk: Gateway and Discord changes can affect channel access, bindings, and system prompts if IDs or configuration patches are wrong. <br>
Mitigation: Back up gateway configuration, confirm every Discord guild and channel ID, and review generated patches before applying them. <br>
Risk: Optional workspace search and channel rename flows may update local files outside the intended scope. <br>
Mitigation: Limit workspace paths to the intended project and review file diffs before committing or deploying changes. <br>
Risk: Cron jobs and long-running agents can continue operating after setup. <br>
Mitigation: Enable scheduled or long-running agents only with a documented stop and cleanup plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/agent-council1) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw agents documentation](https://docs.openclaw.ai/agents) <br>
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with shell, JSON, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands and configuration patches for OpenClaw agent workspaces, gateway settings, Discord channels, and optional scheduled memory updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
