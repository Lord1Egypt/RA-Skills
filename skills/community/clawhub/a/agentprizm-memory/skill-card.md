## Description: <br>
Give your OpenClaw agent persistent, cross-session memory via AgentPrizm so it can recall durable facts, decisions, preferences, lessons, and contacts before acting and store new ones as it learns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentprizm](https://clawhub.ai/user/agentprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent long-term memory for durable facts, decisions, preferences, lessons, contacts, and bookmarks across sessions while keeping memory scoped by container. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected durable memories are sent to a hosted AgentPrizm service and may contain sensitive user or project context if used carelessly. <br>
Mitigation: Install only when hosted memory persistence is acceptable, avoid secrets and regulated or confidential data unless explicitly approved, and periodically review or forget stored memories. <br>
Risk: Memory can bleed between unrelated clients or projects if reads and writes are not scoped carefully. <br>
Mitigation: Use separate containers for separate clients, projects, or environments, and use validity windows for time-sensitive facts. <br>
Risk: A broadened MCP setup can expose AgentPrizm marketplace tools beyond the memory tools needed by this skill. <br>
Mitigation: Keep the default memory_* tool filter unless marketplace access is intentionally required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/agentprizm/skills/agentprizm-memory) <br>
- [AgentPrizm](https://agentprizm.com) <br>
- [AgentPrizm MCP endpoint](https://agentprizm.com/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and MCP server JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTPRIZM_API_KEY; optional AGENTPRIZM_CONTAINER scopes memory containers. The default MCP tool filter exposes memory_* tools only.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and changelog report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
