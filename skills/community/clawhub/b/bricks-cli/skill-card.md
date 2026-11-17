## Description:

Manage BRICKS workspaces through CLI guidance for device status, screenshots, control, monitoring, app and module administration, project setup and deployment, LAN device discovery, MCP debugging, and BRICKS Project Desktop ACP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhen0409](https://clawhub.ai/user/jhen0409)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to manage BRICKS workspace devices, groups, applications, modules, media, and project deployments. It also supports local-network device discovery and BRICKS Project Desktop ACP workflows for debugging and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ACP mode can run project commands without confirmation when auto-approval is enabled.

Mitigation: Use explicit approval or deny-all mode for untrusted prompts, and reserve approve-all mode for isolated trusted projects.

Risk: Persistent acpx configuration can allow future ACP sessions with project file access.

Mitigation: Remove persistent acpx configuration when ACP is not actively needed, especially on shared machines.

Risk: LAN device MCP bridging uses device passcodes as bearer tokens.

Mitigation: Treat passcodes as secrets, avoid logging or committing them, and rotate away from default device passcodes.

Risk: LAN discovery and local device access expose network-connected BRICKS devices to agent workflows.

Mitigation: Run discovery only on trusted networks, verify target workspace membership, and disable ACP or local debugging when idle.

## Reference(s):

- [BRICKS CLI Skill Page](https://clawhub.ai/jhen0409/skills/bricks-cli)
- [BRICKS CLI npm Package](https://www.npmjs.com/package/@fugood/bricks-cli)
- [BRICKS Project Documentation](https://docs.bricks.tools/project)
- [BRICKS Control](https://control.bricks.tools)
- [mcporter](https://mcporter.dev)
- [acpx](https://github.com/openclaw/acpx)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, configuration snippets, workflow steps, and security guidance for BRICKS workspace and device operations.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
