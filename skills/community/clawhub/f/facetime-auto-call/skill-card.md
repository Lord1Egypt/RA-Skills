## Description: <br>
Makes FaceTime audio and video calls via AppleScript automation and handles notification clicking with multi-depth fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keziqicoze09-del](https://clawhub.ai/user/keziqicoze09-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent initiate FaceTime audio or video calls, search local contacts, and configure the macOS Accessibility wrapper needed for UI automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad macOS Accessibility access can let the wrapper control UI outside the immediate FaceTime task. <br>
Mitigation: Grant Accessibility permission only when this automation is intentionally needed, review the scripts first, and remove the generic wrapper if it is not required. <br>
Risk: The skill can start FaceTime calls with too little containment. <br>
Mitigation: Require explicit user confirmation before every call and restrict automated alerts to pre-approved contacts. <br>
Risk: Contact search can read local contact details. <br>
Mitigation: Avoid broad contact search unless needed and prefer direct, user-provided phone numbers or email addresses. <br>
Risk: Notification manipulation can clear or interact with user notifications. <br>
Mitigation: Review whether notification-clearing behavior is necessary and remove that script if the deployment does not require it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keziqicoze09-del/facetime-auto-call) <br>
- [Apple Mac Automation Scripting Guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/) <br>
- [Apple Accessibility Inspector](https://developer.apple.com/documentation/accessibility/accessibility-inspector) <br>
- [OpenClaw Issue #940](https://github.com/openclaw/openclaw/issues/940) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS FaceTime, Contacts, Notification Center, and Accessibility permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
