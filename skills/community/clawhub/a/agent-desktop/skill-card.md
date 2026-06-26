## Description: <br>
Desktop automation via native OS accessibility trees using the agent-desktop CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lahfir](https://clawhub.ai/user/lahfir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill when an agent needs to observe, interact with, or automate desktop applications through the agent-desktop CLI, including reading UI state, clicking controls, filling forms, managing windows, using the clipboard, and taking screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to read and control sensitive parts of a live desktop. <br>
Mitigation: Install it only when desktop automation is intended, grant Accessibility and Screen Recording permissions deliberately, and limit use around private applications or content. <br>
Risk: Screenshots and clipboard operations can expose passwords, private text, or other sensitive content. <br>
Mitigation: Avoid screenshot and clipboard commands around secrets, prefer direct value-setting paths for sensitive text when possible, and clear or inspect the clipboard after automation when appropriate. <br>
Risk: Commands that force-close applications or change system settings can lose work or alter the user environment. <br>
Mitigation: Prefer observe-then-act workflows, verify UI state after each action, and require explicit user intent before force-closing apps or changing settings. <br>


## Reference(s): <br>
- [Agent Desktop on ClawHub](https://clawhub.ai/lahfir/skills/agent-desktop) <br>
- [commands-observation.md](references/commands-observation.md) <br>
- [commands-interaction.md](references/commands-interaction.md) <br>
- [commands-system.md](references/commands-system.md) <br>
- [workflows.md](references/workflows.md) <br>
- [macos.md](references/macos.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing command guidance for desktop observation and action loops.] <br>

## Skill Version(s): <br>
0.1.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
