## Description: <br>
Access a local Dessix desktop workspace by calling the Electron MCP bridge directly from Node.js (socket/pipe), without using MCP stdio JSON-RPC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangst0816](https://clawhub.ai/user/xiangst0816) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to connect to a local Dessix desktop workspace, inspect workspaces and blocks, invoke Dessix tools, and maintain Action or Scene skill content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct read, write, delete, and restore access to a local Dessix workspace. <br>
Mitigation: Use read-only searches first, confirm exact workspace and block IDs, review proposed changes, and require explicit approval before create, update, delete, or restore commands. <br>
Risk: A misconfigured bridge endpoint or active workspace can cause commands to target the wrong local Dessix context. <br>
Mitigation: Check bridge health and the current workspace before invoking tools, and set DESSIX_MCP_BRIDGE_ENDPOINT only to the intended local endpoint. <br>


## Reference(s): <br>
- [Dessix Tool Quick Reference](references/dessix-tools.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiangst0816/dessix-skill) <br>
- [Dessix Skill Homepage](https://github.com/DessixIO/skill) <br>
- [Dessix / OpenClaw Repository](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON bridge responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a reachable local Dessix bridge endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
