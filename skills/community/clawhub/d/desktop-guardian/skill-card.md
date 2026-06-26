## Description: <br>
Desktop Guardian gives OpenClaw agents macOS GUI automation through Hammerspoon, including window and app queries, browser and tab management, dialog handling, keypresses, and policy-based desktop monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[s3rous](https://clawhub.ai/user/s3rous) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent inspect and control a macOS desktop, enforce configurable desktop policies, and surface dialogs or app activity that may need human attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables always-on macOS desktop automation that can close apps, browser windows, tabs, and dialogs automatically. <br>
Mitigation: Install only when that behavior is intended, review the default policy before enabling cleanup, and use ask or disabled actions where automatic cleanup is not acceptable. <br>
Risk: Desktop automation depends on Hammerspoon Accessibility permission and can act on the user's active desktop context. <br>
Mitigation: Grant Accessibility permission only after reviewing the skill, keep the app whitelist narrow, and use the documented kill switch to stop actions immediately. <br>
Risk: The security guidance says to inspect or obtain the missing DesktopGuardian Spoon source before enabling the skill. <br>
Mitigation: Verify the Spoon source and installed files before launch, then confirm cleanup and dialog policies match the user's risk tolerance. <br>


## Reference(s): <br>
- [Hammerspoon Setup Guide](references/hammerspoon-setup.md) <br>
- [macOS Permissions for Desktop Guardian](references/macos-permissions.md) <br>
- [Desktop Guardian Policy Configuration Guide](references/policies.md) <br>
- [Hammerspoon](https://www.hammerspoon.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration, and JSON-oriented command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Hammerspoon Accessibility permission for full control, and optional Chrome DevTools Protocol access for tab-level browser actions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
