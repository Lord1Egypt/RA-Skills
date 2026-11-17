## Description:

Make FaceTime audio/video calls via AppleScript. Automatically handles notification clicking with multi-depth fallback. Use when user wants to call someone or set up automated call alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keziqicoze09-del](https://clawhub.ai/user/keziqicoze09-del)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents on macOS use this skill to start FaceTime audio or video calls, find contacts, or configure automated call alerts when they can grant the required Accessibility permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent macOS Accessibility authority through a generic NodeRunner.app wrapper.

Mitigation: Grant the permission only on trusted machines, review the setup script first, and revoke Accessibility access when the skill is no longer needed.

Risk: The call script can initiate real FaceTime audio or video calls and automatically click the confirmation notification.

Mitigation: Require explicit user confirmation before each call and restrict automated use to trusted contacts and alerting workflows.

Risk: Contact search and notification-clearing behavior may expose local contact data or alter Notification Center state.

Mitigation: Review or remove those scripts when they are not required for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keziqicoze09-del/skills/facetime-auto-call)
- [Apple Mac Automation Scripting Guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/)
- [Apple Accessibility Inspector](https://developer.apple.com/documentation/accessibility/accessibility-inspector)
- [OpenClaw Issue #940](https://github.com/openclaw/openclaw/issues/940)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands accept audio, video, find-contact, and test modes with a phone number, email address, or contact query.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
