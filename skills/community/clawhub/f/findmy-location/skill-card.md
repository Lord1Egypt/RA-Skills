## Description: <br>
Track a shared contact's location via Apple Find My with street-level accuracy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poiley](https://clawhub.ai/user/poiley) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users on macOS use this skill to query the Apple Find My app for a consenting shared contact's current location, map context, and whether additional vision-based reading is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose precise live location information for a shared contact. <br>
Mitigation: Use it only for contacts who intentionally share location with the configured Apple account, and configure the target contact carefully. <br>
Risk: The skill requires screen-reading and UI-control permissions, and can capture Find My screenshots under /tmp. <br>
Mitigation: Close sensitive windows before running, grant permissions only if acceptable, and delete temporary screenshots after use. <br>
Risk: The optional Hammerspoon click helper uses a local unauthenticated HTTP endpoint for UI clicking. <br>
Mitigation: Avoid the helper unless necessary, and restrict, disable, or remove it when not in use. <br>


## Reference(s): <br>
- [Find My Location on ClawHub](https://clawhub.ai/poiley/findmy-location) <br>
- [peekaboo](https://github.com/steipete/peekaboo) <br>
- [Hammerspoon](https://www.hammerspoon.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON command output with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a local screenshot path when vision analysis is needed.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
