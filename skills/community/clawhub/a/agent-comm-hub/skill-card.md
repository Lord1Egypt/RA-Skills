## Description: <br>
Agent Comm Hub is a multi-agent communication and context-sharing hub that exposes MCP tools, SSE and WebSocket event streams, and local SQLite persistence for agent messaging, task coordination, shared memory, and file transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local coordination hub for MCP-compatible agents that need to exchange messages, assign tasks, share temporary memory, transfer files, and receive real-time events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hub handles cross-agent messages, tasks, files, memory, and diagnostics that may be broader than the documentation's stated isolation model. <br>
Mitigation: Install only in a trusted local environment, review permissions before connecting agents, and avoid using it for sensitive shared data until access boundaries are verified. <br>
Risk: Exposing the hub service on port 3100 can make agent coordination data reachable outside the intended local environment. <br>
Mitigation: Bind the server to localhost or place it behind a firewall, and do not expose port 3100 publicly. <br>
Risk: Optional watcher and runner scripts can automate local operations before their behavior is fully reviewed. <br>
Mitigation: Keep optional watcher and runner scripts disabled until reviewed in the target deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuboacean/agent-comm-hub) <br>
- [README](README.md) <br>
- [English README](docs/README_EN.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Advanced Orchestration Guide](docs/advanced-orchestration-guide.md) <br>
- [Hub DB Split Three-Layer Protection](docs/hub-db-split-three-layer-protection.md) <br>
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, TypeScript, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool calls, local server commands, configuration snippets, and operational checklists.] <br>

## Skill Version(s): <br>
3.0.10 (source: server release evidence, created 2026-05-26T08:36:20Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
