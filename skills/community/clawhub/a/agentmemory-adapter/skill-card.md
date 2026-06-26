## Description: <br>
Installs, wires, audits, and hardens AgentMemory integrations for Codex, OpenClaw, ClawHub skill work, and project workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install or audit AgentMemory and configure reliable memory support for coding agents across Codex, OpenClaw, and project workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and agent configuration changes can retain sensitive context or affect future sessions. <br>
Mitigation: Install only when persistent coding-agent memory is desired, avoid storing secrets in memory, and review generated configuration and hooks after setup. <br>
Risk: Bearer-token-protected AgentMemory servers can expose credentials if tokens are sent over non-loopback HTTP. <br>
Mitigation: Use localhost or HTTPS for protected servers and set AGENTMEMORY_REQUIRE_HTTPS=1 when unsafe routes should fail closed. <br>
Risk: Shared memory can cross role boundaries in sensitive or multi-agent work. <br>
Mitigation: Enable isolated agent scope for sensitive or multi-role workflows. <br>
Risk: MCP fallback mode can appear functional while exposing only a limited tool surface. <br>
Mitigation: Start and verify the live AgentMemory server and run the bundled diagnostic script before and after configuration changes. <br>


## Reference(s): <br>
- [AgentMemory Adapter ClawHub page](https://clawhub.ai/zack-dev-cm/agentmemory-adapter) <br>
- [Publisher profile: zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>
- [AgentMemory Adapter homepage](https://github.com/zack-dev-cm/agentmemory-skills) <br>
- [AgentMemory upstream repository](https://github.com/rohitg00/agentmemory) <br>
- [AgentMemory Deep Analysis](references/agentmemory-deep-analysis.md) <br>
- [Platform Recipes](references/platform-recipes.md) <br>
- [Source Manifest](references/source-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON/TOML/YAML snippets, and diagnostic output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect local Codex/OpenClaw configuration and AgentMemory endpoints; should avoid printing secrets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and source-manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
