## Description: <br>
Set up and use an MCP message broker for direct inter-agent communication between OpenClaw and other AI agents, such as hermes-agent, Claude Code, or any MCP-capable agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryno2390](https://clawhub.ai/user/ryno2390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a local bridge so two MCP-capable agents on the same machine can exchange task messages without manual copy-paste relay. It supports a FastMCP and SQLite broker, with a filesystem inbox fallback when the MCP server is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge creates a persistent local message channel and stores messages in SQLite or shared JSON files. <br>
Mitigation: Use only on trusted single-user machines, avoid sending secrets, and periodically delete or rotate the message database and shared inbox files. <br>
Risk: Heartbeat auto-processing can cause agents to act on messages from any local process or agent with access to the inbox or localhost broker. <br>
Mitigation: Enable auto-processing only when every local writer and MCP client is trusted; otherwise require manual review before processing incoming messages. <br>
Risk: launchd auto-start can keep the broker running longer than intended. <br>
Mitigation: Keep stop and unload steps available, review the plist paths before loading, and disable the service when the bridge is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryno2390/agent-mcp-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/ryno2390) <br>
- [Filesystem Bridge](references/filesystem-bridge.md) <br>
- [launchd plist](references/launchd-plist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JSON configuration examples, bash commands, Python snippets, and plist configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite message storage, filesystem inbox files, and launchd service configuration when followed by an agent or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
