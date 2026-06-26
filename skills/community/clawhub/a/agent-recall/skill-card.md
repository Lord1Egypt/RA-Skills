## Description: <br>
AgentRecall provides local, persistent memory for AI agents through MCP tools, hooks, commands, and markdown/JSON stores for sessions, recalls, corrections, and cross-project insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldentrii](https://clawhub.ai/user/goldentrii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use AgentRecall to preserve project memory, corrections, decisions, and recall context across recurring AI-agent sessions. It is intended for local-first workflows where agents need durable notes, cross-project insights, and session continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable local memory can retain agent-readable long-term notes, including sensitive information if users store it. <br>
Mitigation: Do not store secrets or credentials, and periodically inspect or purge ~/.agent-recall. <br>
Risk: Hooks, /arsaveall, and sync-memory expand access beyond the narrow default MCP workflow by reading prompts, transcripts, or memory files. <br>
Mitigation: Start with the default MCP server and avoid enabling hooks, /arsaveall, or sync-memory until their access patterns are understood. <br>
Risk: Some workflows include shell-driven commands and deletion behavior. <br>
Mitigation: Review generated commands before execution and require explicit human confirmation before destructive operations. <br>
Risk: Installing through floating package commands can change the code that runs in future sessions. <br>
Mitigation: Pin package versions where possible and review updates before deployment. <br>


## Reference(s): <br>
- [AgentRecall ClawHub page](https://clawhub.ai/goldentrii/agent-recall) <br>
- [agent-recall-mcp npm package](https://www.npmjs.com/package/agent-recall-mcp) <br>
- [agent-recall-sdk npm package](https://www.npmjs.com/package/agent-recall-sdk) <br>
- [agent-recall-cli npm package](https://www.npmjs.com/package/agent-recall-cli) <br>
- [Command Reference](docs/commands.md) <br>
- [Recall Scoring Design Rationale](docs/SCORING.md) <br>
- [MCP Adapter Interface Specification](docs/mcp-adapter-spec.md) <br>
- [Intelligent Distance Protocol](docs/intelligent-distance-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, shell commands, JSON/YAML configuration examples, and local markdown/JSON memory artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs and stored memory are local-first; persistent notes may remain agent-readable until inspected, archived, or purged.] <br>

## Skill Version(s): <br>
3.3.27 (source: server release, SKILL.md frontmatter, package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
