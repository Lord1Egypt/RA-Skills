## Description: <br>
Manage BRICKS workspaces and local BRICKS devices through CLI commands for device control, app/module/media management, project setup, LAN discovery, MCP bridging, and Desktop ACP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhen0409](https://clawhub.ai/user/jhen0409) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to operate BRICKS workspaces, deploy and manage applications or modules, inspect device state, and connect local BRICKS Foundation devices or BRICKS Project Desktop sessions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LAN discovery and device MCP bridging can interact with BRICKS devices on the local network. <br>
Mitigation: Use the skill only on trusted networks and confirm that discovered devices belong to the intended workspace before connecting or dispatching actions. <br>
Risk: Device MCP bridging uses passcodes as bearer tokens. <br>
Mitigation: Treat passcodes as secrets, avoid logging or committing them, and rotate them if exposed. <br>
Risk: Desktop ACP sessions can execute commands in a BRICKS project context. <br>
Mitigation: Keep ACP disabled when idle and prefer interactive approvals or deny-all mode for untrusted prompts. <br>
Risk: Persistent acpx configuration can make future ACP sessions easier to start from the same machine. <br>
Mitigation: Remove persistent acpx configuration when ACP access is no longer actively needed, especially on shared systems. <br>


## Reference(s): <br>
- [BRICKS CLI npm package](https://www.npmjs.com/package/@fugood/bricks-cli) <br>
- [BRICKS Project Desktop documentation](https://docs.bricks.tools/project) <br>
- [mcporter](https://mcporter.dev) <br>
- [acpx Agent Client Protocol CLI](https://github.com/openclaw/acpx) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may produce JSON output when run with -j or --json.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
