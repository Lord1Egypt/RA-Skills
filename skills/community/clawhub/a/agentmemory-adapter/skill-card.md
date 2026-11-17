## Description:

Installs, wires, audits, and hardens AgentMemory integrations for Codex, OpenClaw, and project workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, configure, verify, and troubleshoot AgentMemory as a persistent shared memory layer across Codex, OpenClaw, and project workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally installs persistent shared memory and hook/plugin integrations that can capture or inject agent context.

Mitigation: Install only when persistent shared memory is intended, review Codex/OpenClaw config and hook changes before accepting them, and use isolated agent scope or deletion workflows only with explicit user approval.

Risk: Bearer-token handling can expose AGENTMEMORY_SECRET when used with untrusted or plaintext non-loopback endpoints.

Mitigation: Use trusted local or HTTPS AgentMemory endpoints, avoid setting AGENTMEMORY_SECRET unless required, set AGENTMEMORY_REQUIRE_HTTPS=1 for strict transport checks, and rotate the secret if it may have been used with an untrusted endpoint.

Risk: MCP fallback mode can appear operational while exposing only a reduced memory tool surface.

Mitigation: Verify the AgentMemory server is reachable, prefer proxy mode with a live server for the full tool surface, and run the bundled diagnostic script before and after configuration changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/agentmemory-adapter)
- [AgentMemory Adapter Homepage](https://github.com/zack-dev-cm/agentmemory-skills)
- [Upstream AgentMemory Repository](https://github.com/rohitg00/agentmemory)
- [AgentMemory Deep Analysis](references/agentmemory-deep-analysis.md)
- [Platform Recipes](references/platform-recipes.md)
- [Source Manifest](references/source-manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and diagnostic interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Codex/OpenClaw MCP, hook, plugin, and environment configuration changes; diagnostic guidance avoids printing AGENTMEMORY_SECRET.]

## Skill Version(s):

1.0.3 (source: server release metadata and references/source-manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
