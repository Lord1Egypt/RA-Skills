## Description: <br>
Use when the user wants to update Claude settings, hooks, permissions, MCP server toggles, or other JSON config safely and with scope awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to make targeted edits to Claude settings, local overrides, hooks, permissions, plugins, and MCP server configuration while preserving valid JSON and respecting settings scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Settings, hooks, permissions, plugins, and MCP server changes can persist and alter future Claude behavior. <br>
Mitigation: Review the exact JSON diff, use the narrowest settings scope that solves the problem, and treat broad permission or automation-hook changes as sensitive. <br>


## Reference(s): <br>
- [Claude Settings Editor on ClawHub](https://clawhub.ai/wimi321/claude-code-claude-settings-editor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON configuration edits or shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on minimal, scope-aware settings changes and asks the agent to explain risky configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
