## Description:

Persistent cross-session memory for OpenClaw agents through an agentmemory MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lufei4](https://clawhub.ai/user/lufei4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, configure, verify, troubleshoot, upgrade, or remove agentmemory-backed long-term memory. Agents can use the guidance to enable recall, saving, migration from MEMORY.md, and hybrid memory search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background execution and automatic conversation capture can store sensitive or unintended session content.

Mitigation: Keep the service local, review captured memories regularly, and disable or restrict automatic capture when handling sensitive work.

Risk: Docker-level access increases the impact of a compromised or misconfigured memory service.

Mitigation: Avoid Docker socket access unless the service is fully trusted, and use pinned package and image versions for installation.

Risk: Recalled or imported memories may contain stale, incorrect, or instruction-like content.

Mitigation: Treat recalled memories as untrusted reference material, review MEMORY.md before import, and verify memory-derived claims before acting on them.

Risk: Network-facing memory endpoints could expose stored context if bound beyond localhost.

Mitigation: Keep the memory server bound to localhost and avoid exposing ports 3111 or 3113 to untrusted networks.

## Reference(s):

- [agentmemory MCP Tools Reference](references/mcp-tools.md)
- [agentmemory and MEMORY.md Coordination Guide](references/coordination.md)
- [OpenClaw Plugin Manifest](references/openclaw-plugin/openclaw.plugin.json)
- [OpenClaw Plugin Package Metadata](references/openclaw-plugin/package.json)
- [OpenClaw Plugin Source](references/openclaw-plugin/plugin.mjs)
- [ClawHub skill page](https://clawhub.ai/lufei4/skills/agentmemory-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, configuration, verification, troubleshooting, migration, and removal guidance for an OpenClaw memory integration.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
