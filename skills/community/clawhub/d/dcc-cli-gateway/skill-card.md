## Description: <br>
Default unified entry for agents and headless CLI hosts to control live DCC applications through dcc-mcp-cli local registry/direct MCP or remote gateway REST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical artists, and shell-capable agent hosts use this skill to inventory DCC instances, discover tool schemas, and invoke DCC-MCP tools through a CLI-first workflow with a REST fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to download dcc-mcp-cli from GitHub releases or use installer commands when setup paths are needed. <br>
Mitigation: Require explicit user consent before downloads or setup, verify the release source, and inspect installer commands before running them. <br>
Risk: The skill can start persistent local gateway daemons, install adapters or marketplace skills, and mutate local DCC environments. <br>
Mitigation: Use inventory and doctor commands first, review planned changes, and require approval before executing install, marketplace, daemon, or adapter setup commands. <br>
Risk: Remote gateway profiles can route commands to a workstation or studio service outside the local machine. <br>
Mitigation: Confirm any remote gateway URL belongs to the user or studio before selecting the profile or invoking tools through it. <br>


## Reference(s): <br>
- [DCC CLI Gateway source](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-cli-gateway/SKILL.md) <br>
- [CLI cheatsheet](references/CLI_CHEATSHEET.md) <br>
- [Zero instances CLI setup guide](references/ZERO_INSTANCES_CLI.md) <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/skills/dcc-cli-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands that inspect local or remote DCC gateway state, request consent before setup, and return JSON from dcc-mcp-cli or the Python REST fallback.] <br>

## Skill Version(s): <br>
0.19.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
