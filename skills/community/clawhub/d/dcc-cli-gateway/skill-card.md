## Description: <br>
Enables shell-capable agents and headless CLI hosts to inventory DCC instances and search, describe, or call DCC-MCP tools through dcc-mcp-cli or a Python REST fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical artists, and agent operators use this skill to let shell-capable agents control live DCC applications through an inventory, search, describe, and call workflow. It is intended for agent and headless CLI hosts rather than MCP-native IDE clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run CLI commands that control DCC tools, local daemons, gateway profiles, and marketplace operations. <br>
Mitigation: Require user consent before setup, downloads, adapter execution, daemon or profile changes, and marketplace install or update commands; inspect tool schemas before calls. <br>
Risk: Installer paths and CLI download flows are privileged setup actions. <br>
Mitigation: Use --ensure-cli, vx installation, adapter --execute, and release downloads only when the user trusts the source, gateway URL, and local environment. <br>
Risk: Remote gateway profiles can target external DCC environments and cannot be auto-started locally. <br>
Mitigation: Confirm the selected profile or gateway URL, report unreachable remotes clearly, and ask permission before troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/skills/dcc-cli-gateway) <br>
- [Skill homepage](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-cli-gateway/SKILL.md) <br>
- [CLI cheatsheet](references/CLI_CHEATSHEET.md) <br>
- [Zero instances CLI setup guide](references/ZERO_INSTANCES_CLI.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return JSON from dcc-mcp-cli or the Python REST fallback.] <br>

## Skill Version(s): <br>
0.19.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
