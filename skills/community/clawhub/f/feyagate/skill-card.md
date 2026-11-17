## Description:

MCP smart home gateway for AI agents. Control Xiaomi, Tuya, Midea, eWeLink, cameras, and XiaoAI speakers via MCP protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toddpan](https://clawhub.ai/user/toddpan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use Feyagate to connect AI agents to a local MCP/HTTP gateway for supported device discovery, authorization, control, camera access, automation, and configuration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-install instructions and binary download can execute code that has not been independently reviewed.

Mitigation: Review the installer and binary source first, prefer pinned versions with checksums, and require explicit approval before running one-line install commands.

Risk: The gateway can expose smart-home controls, account credentials, camera data, and Vision AI settings.

Mitigation: Run the gateway on localhost only, keep it behind a firewall, and avoid entering account passwords over non-loopback HTTP.

Risk: Camera/Vision AI, schedules, memory, and skill-management tools can create persistent or sensitive changes.

Mitigation: Treat those tools as admin-only actions and require explicit user approval before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toddpan/skills/feyagate)
- [Server-resolved GitHub provenance](https://github.com/toddpan/feyagate-skill)
- [Feyagate homepage](https://www.feyagate.com)
- [Quick Start Guide](artifact/QUICKSTART.md)
- [FeyaGate MCP API](artifact/FeyaGate_MCP_API.md)
- [FeyaGate HTTP API](artifact/FeyaGate_HTTP_API.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with command snippets, JSON tool-call examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate MCP/HTTP requests and smart-home device actions through a local gateway after user authorization.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter reports 1.2.31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
