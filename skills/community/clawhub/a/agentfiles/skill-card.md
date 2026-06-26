## Description: <br>
Use this skill when you need to publish, fetch, search, list, share, or watch AgentFiles artifacts from Codex, Claude Code, OpenClaw, or other agent runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hammadtq](https://clawhub.ai/user/hammadtq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use AgentFiles to move artifacts, handoff messages, and shared context across Codex, Claude Code, OpenClaw, and other runtimes through the AgentFiles CLI or MCP-backed handoff flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can publish, share, or hand off content from the configured AgentFiles account. <br>
Mitigation: Confirm the namespace, recipient, artifact ID, and whether the content contains secrets or private data before publishing or sharing. <br>
Risk: Fetching artifacts with an output path can write content to local files. <br>
Mitigation: Confirm artifact IDs and local output paths before using download or write options. <br>
Risk: Watch automation can run local executables for emitted events. <br>
Mitigation: Use trusted executable paths only and review watch behavior before enabling exec-based automation. <br>
Risk: The skill depends on the AgentFiles CLI or npm package and local AgentFiles credentials. <br>
Mitigation: Install only when the CLI package is trusted and the user intends the agent to use the configured AgentFiles account. <br>


## Reference(s): <br>
- [AgentFiles homepage](https://agentfiles.io) <br>
- [ClawHub AgentFiles release](https://clawhub.ai/hammadtq/agentfiles) <br>
- [AgentFiles Command Matrix](references/commands.md) <br>
- [AgentFiles Runtime Notes](references/runtime-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with AgentFiles CLI commands and handoff content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish, fetch, share, or watch artifacts through the configured AgentFiles account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
