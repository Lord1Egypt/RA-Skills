## Description: <br>
Integrates MCP tool servers for orchestration, state persistence with IndexedDB/localStorage, and session sync across devices in OpenClaw/Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enderfga](https://clawhub.ai/user/Enderfga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers building OpenClaw or Claude Code integrations use this skill to manage MCP tool servers, persist local agent state, and merge chat or configuration state across sessions and devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP servers may receive broad local execution context, filesystem access, environment variables, or account tokens. <br>
Mitigation: Install only trusted and pinned MCP server packages, restrict filesystem roots and token scopes, and run with a minimal environment. <br>
Risk: Tool calls can read files, write files, or act on external accounts depending on the configured server. <br>
Mitigation: Require user confirmation before adding servers or executing sensitive tool calls. <br>
Risk: Tokens placed in MCP configuration files can be exposed to configured servers or local readers. <br>
Mitigation: Avoid hardcoding secrets in config files and prefer narrowly scoped credentials supplied through a controlled environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Enderfga/claude-code-skill) <br>
- [npm Package](https://www.npmjs.com/package/openclaw-claude-code-skill) <br>
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [TypeScript APIs, JSON configuration examples, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP server orchestration helpers and persistent state utilities for agent applications.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
