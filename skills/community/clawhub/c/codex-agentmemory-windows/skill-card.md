## Description: <br>
Configure, repair, and validate agentmemory integration for Codex App on Windows. Use when Codex needs to set up agentmemory hooks, fix Windows PowerShell hook failures, create an agentmemory-hook.cmd wrapper, update ~/.codex/hooks.json and trusted_hash entries, fix missing Codex additionalContext memory injection, repair stale/frozen agentmemory knowledge graph updates, backfill graph nodes/edges, or troubleshoot Codex App agentmemory MCP/hook configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyun2000](https://clawhub.ai/user/yuyun2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure, repair, and validate agentmemory hooks, memory injection, and graph updates for Codex App on Windows. It supports both automated repair through bundled scripts and manual troubleshooting of Codex hook and agentmemory service configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist Codex activity into agentmemory and modifies Codex hook and configuration files. <br>
Mitigation: Run dry-run first and review all changes to hooks.json and config.toml before applying them. <br>
Risk: The Codex home directory can contain the agentmemory bearer secret after configuration. <br>
Mitigation: Protect ~/.codex and keep the agentmemory endpoint local or otherwise under the user's control. <br>
Risk: The graph repair workflow can restart services on ports 3111 and 3113. <br>
Mitigation: Avoid --restart-service until confirming those ports belong to agentmemory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyun2000/codex-agentmemory-windows) <br>
- [Publisher profile](https://clawhub.ai/user/yuyun2000) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with PowerShell, cmd, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Windows-focused setup and repair instructions for Codex App and agentmemory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
