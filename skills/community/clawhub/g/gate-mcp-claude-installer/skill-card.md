## Description: <br>
Gate MCP and Gate skills installer for Claude Code (CLI). Use when the user asks to install Gate tools in Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to install selected Gate MCP endpoints and the Gate skills bundle, merge them into user-level Claude configuration, and receive post-install restart and authorization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make broad persistent changes to user-level Claude configuration and installed skills. <br>
Mitigation: Review the exact ~/.claude.json and ~/.claude/skills changes before installation, back up existing skills, and select only the MCPs needed. <br>
Risk: The skill configures crypto and account-related MCP endpoints that may later require API keys, bearer tokens, or OAuth authorization. <br>
Mitigation: Do not place real exchange API keys or bearer tokens into shared files or chat, and install only when Gate MCP services are intended for the user's Claude setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-mcp-claude-installer) <br>
- [Gate Claude Installer MCP Specification](artifact/references/mcp.md) <br>
- [Gate MCP](https://github.com/gate/gate-mcp) <br>
- [Gate skills](https://github.com/gate/gate-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide manual configuration snippets when automatic installation fails.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
