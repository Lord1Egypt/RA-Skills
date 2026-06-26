## Description: <br>
Persistent semantic memory layer for AI agents with local-first storage, semantic search, typed memories, relationships, scoped recall, import/export, REST API, and MCP support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dannydvm](https://clawhub.ai/user/Dannydvm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Engram to give AI agents durable local memory across sessions, including facts, decisions, preferences, events, relationships, and context-aware recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable local memory may store sensitive information, including credentials or confidential conversation content. <br>
Mitigation: Do not store passwords, API keys, tokens, regulated data, or raw confidential conversations in Engram. <br>
Risk: The local memory server and MCP integration may expose stored memories to tools or clients that can access them. <br>
Mitigation: Keep the server bound to localhost and restrict which tools and MCP clients can access the memory store. <br>
Risk: The documented decay model archives low-salience memories rather than fully deleting them. <br>
Mitigation: Treat archived memories as retained data and review deletion, export, and retention practices before storing sensitive material. <br>


## Reference(s): <br>
- [Engram ClawHub listing](https://clawhub.ai/Dannydvm/engram) <br>
- [Engram README](https://github.com/Dannydvm/engram-memory/blob/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to store, search, recall, relate, import, export, and configure local semantic memories.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
