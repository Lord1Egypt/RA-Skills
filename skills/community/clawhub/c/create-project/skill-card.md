## Description: <br>
Interactive Orchestrix project scaffolding that creates a project directory, generates a project brief from Q&A, installs MCP configuration, hooks, slash commands, tmux scripts, and initializes git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorayo](https://clawhub.ai/user/dorayo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to start a new Orchestrix workspace from an interactive planning interview. It produces a project brief, local project structure, Claude Code commands and hooks, MCP configuration, tmux automation scripts, and initial git setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Orchestrix-specific Claude Code hooks and tmux automation that can auto-accept trust or approval prompts. <br>
Mitigation: Review and remove auto-accept or auto-approve logic before use, and inspect .claude/settings.local.json and .orchestrix-core scripts. <br>
Risk: The generated project can place an Orchestrix license key in .mcp.json and commit generated project files. <br>
Mitigation: Keep .mcp.json and license keys out of git, use placeholders or secrets management, and review git contents before committing. <br>
Risk: Created tmux sessions and hooks may continue routing agent workflow commands after setup. <br>
Mitigation: Stop or remove the created tmux sessions and hooks when automation is no longer needed. <br>


## Reference(s): <br>
- [Create Project on ClawHub](https://clawhub.ai/dorayo/create-project) <br>
- [Orchestrix homepage](https://orchestrix-mcp.youlidao.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated project/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local project files under the user's project directory and may initialize git when run by an agent.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
