## Description: <br>
Persistent cross-session memory for OpenClaw via agentmemory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lufei4](https://clawhub.ai/user/lufei4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, verify, troubleshoot, and remove an agentmemory MCP setup for OpenClaw. It helps agents recall project context, decisions, workflows, and prior sessions through local memory tools and optional embedding-backed search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports cross-session memory and includes plugin behavior that can recall and capture session context. <br>
Mitigation: Enable it only when persistent memory is intended, review captured content, and confirm how to disable capture and delete stored entries. <br>
Risk: Optional vector search may send text to an external embedding provider when API keys and provider settings are configured. <br>
Mitigation: Use the default BM25-only mode for local-only search, or review the selected provider, endpoint, data handling terms, and redaction process before enabling embeddings. <br>
Risk: Stored memories can contain secrets, customer data, regulated information, or private conversations if users or agents save them. <br>
Mitigation: Do not save sensitive material without review and redaction, and establish deletion and audit practices before production use. <br>


## Reference(s): <br>
- [agentmemory-mcp ClawHub Page](https://clawhub.ai/lufei4/agentmemory-mcp) <br>
- [agentmemory MCP Tools Reference](references/mcp-tools.md) <br>
- [agentmemory and MEMORY.md Coordination Guide](references/coordination.md) <br>
- [OpenClaw Plugin Manifest](references/openclaw-plugin/openclaw.plugin.json) <br>
- [OpenClaw Plugin Implementation](references/openclaw-plugin/plugin.mjs) <br>
- [Verification Script](scripts/verify.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and plugin code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that start local services, configure OpenClaw MCP, inspect health endpoints, manage systemd user services, and configure optional embedding providers.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
