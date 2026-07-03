## Description: <br>
Desktop automation via native OS accessibility trees using the agent-desktop CLI for observing, interacting with, and automating desktop applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lahfir](https://clawhub.ai/user/lahfir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect desktop UI state and perform controlled GUI actions such as clicking, typing, navigating menus, handling windows, reading notifications, and managing clipboard or screenshot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful local desktop control through accessibility permissions, including actions that can modify applications and windows. <br>
Mitigation: Install only when desktop automation is intended, grant Accessibility and Screen Recording permissions carefully, and use headed or forceful actions only for deliberate high-impact operations. <br>
Risk: Screenshot, clipboard, and trace workflows can expose sensitive local information. <br>
Mitigation: Avoid clipboard or screenshot workflows around secrets, prefer no-trace sessions for sensitive work, and run session garbage collection after completing automation. <br>


## Reference(s): <br>
- [Agent Desktop Skill Page](https://clawhub.ai/lahfir/skills/agent-desktop) <br>
- [Observation Commands](references/commands-observation.md) <br>
- [Interaction Commands](references/commands-interaction.md) <br>
- [System Commands](references/commands-system.md) <br>
- [Common Automation Workflows](references/workflows.md) <br>
- [macOS Platform](references/macos.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on the agent-desktop CLI, structured JSON command envelopes, snapshot refs, and macOS permission workflows.] <br>

## Skill Version(s): <br>
0.1.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
