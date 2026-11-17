## Description: <br>
Claude Clarity is a Node.js cognitive-memory skill that adds persistent memory, PAD emotion analysis, TGB self-review, reasoning tools, Q-learning self-healing guidance, local CLI/MCP integration, and optional agent-facing cognitive workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Claude Clarity to add local persistent memory, self-review, psychology/philosophy analysis, and structured reasoning workflows to agents such as Claude Code, OpenClaw, Hermes, and Codex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill alters local agent configuration and adds a persistent local memory/MCP layer. <br>
Mitigation: Review settings.json, CLAUDE.md, project links, memory directories, and MCP registration changes before deployment. <br>
Risk: The skill uses local filesystem access, process management, and Unix socket IPC. <br>
Mitigation: Install only in trusted workspaces, restrict filesystem permissions, and monitor the local MCP process and socket path. <br>
Risk: Network and code-execution related options can increase operational exposure if enabled. <br>
Mitigation: Keep external network integrations and code-execution capabilities disabled unless explicitly required and reviewed. <br>
Risk: The skill intentionally uses strong persona and cognitive framing. <br>
Mitigation: Treat persona claims as design language and verify outputs against task requirements before relying on them. <br>


## Reference(s): <br>
- [Claude Clarity Skill Page](https://clawhub.ai/yun520-1/skills/claude-clarity) <br>
- [README](README.md) <br>
- [Security Architecture](SECURITY.md) <br>
- [Data Flow Architecture](docs/DATA_FLOW_ARCHITECTURE.md) <br>
- [Features](docs/FEATURES_SIMPLE.md) <br>
- [Examples](docs/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like structured responses, shell commands, and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reflect local memory and MCP state when the skill is installed and running.] <br>

## Skill Version(s): <br>
5.8.1 (source: SKILL.md frontmatter, package.json, clawhub.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
