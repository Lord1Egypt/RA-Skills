## Description: <br>
Desktop automation via native OS accessibility trees using the agent-desktop CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarryEK](https://clawhub.ai/user/DarryEK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to observe and control macOS desktop applications through accessibility trees, including form filling, menu navigation, window management, notifications, screenshots, and clipboard operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad control over local desktop applications. <br>
Mitigation: Install it only for intentional desktop-control workflows and grant Accessibility permission from a dedicated terminal profile where possible. <br>
Risk: The skill can expose sensitive local context through screenshots, clipboard access, notifications, and visible application state. <br>
Mitigation: Keep sensitive applications closed and require explicit approval before reading screenshots, clipboard contents, notifications, or UI state from sensitive apps. <br>
Risk: The skill can click destructive controls, submit data, close apps, or change settings. <br>
Mitigation: Require review before actions that submit data, change settings, close applications, dismiss notifications, or activate destructive UI controls. <br>
Risk: The installation flow depends on an external agent-desktop package. <br>
Mitigation: Verify the external package before global installation and avoid using --trust unless its install scripts are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DarryEK/aoto) <br>
- [Observation Commands](references/commands-observation.md) <br>
- [Interaction Commands](references/commands-interaction.md) <br>
- [System Commands](references/commands-system.md) <br>
- [Common Automation Workflows](references/workflows.md) <br>
- [macOS Platform](references/macos.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS 12+ and Accessibility permission for desktop control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
