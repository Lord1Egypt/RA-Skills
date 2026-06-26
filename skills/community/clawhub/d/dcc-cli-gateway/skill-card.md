## Description: <br>
DCC CLI Gateway guides shell-capable agents and headless hosts to inventory DCC instances and search, describe, and call DCC-MCP tools through dcc-mcp-cli or a Python REST fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical directors, and agent operators use this skill when a shell-capable agent needs to control live DCC applications through a CLI workflow instead of a native MCP connector. It helps agents check instance inventory, inspect tool schemas, call DCC tools, and handle zero-instance setup with user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports weak verification safeguards around installing and running downloaded DCC-MCP tooling. <br>
Mitigation: Install only from trusted dcc-mcp releases, verify the release source before using installer commands, prefer pinned versions and checksums where available, and avoid pipe-to-shell installs. <br>
Risk: The skill can guide an agent to control local or remote DCC applications, which may affect live creative workstations or project files. <br>
Mitigation: Require explicit user consent before setup, installation, remote troubleshooting, or tool calls that change DCC state; use HTTPS for non-local gateway endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/dcc-cli-gateway) <br>
- [Homepage from skill metadata](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-cli-gateway/SKILL.md) <br>
- [CLI cheatsheet](references/CLI_CHEATSHEET.md) <br>
- [Zero instances setup guide](references/ZERO_INSTANCES_CLI.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents are expected to ask for consent before installer or setup actions and to inspect returned JSON before calling tools.] <br>

## Skill Version(s): <br>
0.18.39 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
