## Description: <br>
Claude Clarity is a Node.js cognitive engine and local MCP integration toolkit that provides persistent memory, structured reasoning and self-verification, PAD emotion analysis, TGB evaluation, and Q-learning self-healing utilities for supported agent environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Claude Clarity to add a local memory, reasoning, self-checking, and MCP tool layer to Claude Code, OpenClaw, Hermes, Codex, or compatible local agent workflows. It is intended for users who want local cognitive-analysis utilities that can be installed, started, queried, and managed from command-line or MCP-enabled environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can modify user-level Claude MCP settings, create local links, and start helper processes. <br>
Mitigation: Review install prompts and configuration changes before installation, and install only in environments where local MCP integration is intended. <br>
Risk: The skill maintains local memory, configuration, and log state that may contain user or workflow context. <br>
Mitigation: Review local storage paths and retention expectations, and avoid storing sensitive data unless the deployment policy allows it. <br>
Risk: Code-execution-related modules exist in the artifact and have sandbox limits even though the security evidence says they are gated. <br>
Mitigation: Keep code execution disabled unless explicitly needed, understand the sandbox limits, and review generated or proposed code before running it. <br>
Risk: Optional external embeddings or LLM endpoints can transmit data when intentionally enabled. <br>
Mitigation: Enable external endpoints only with deliberate configuration and confirm the destination, data handling, and credential policy first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yun520-1/skills/claude-clarity) <br>
- [README](README.md) <br>
- [Security Architecture](SECURITY.md) <br>
- [System Requirements](SYSTEM_REQUIREMENTS.md) <br>
- [Data Flow Architecture](docs/DATA_FLOW_ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or text responses with optional JSON status output, JavaScript examples, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory, configuration, and log state and may manage local MCP helper processes when installed.] <br>

## Skill Version(s): <br>
1.8.12 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
