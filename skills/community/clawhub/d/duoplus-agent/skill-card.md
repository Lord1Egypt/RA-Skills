## Description:

Control Android cloud phones via ADB broadcast commands for tapping, swiping, typing, screenshots, and UI element inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duoplusofficial](https://clawhub.ai/user/duoplusofficial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to connect to authorized DuoPlus Android cloud phones and perform UI automation tasks such as launching apps, entering text, navigating screens, and capturing screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control an Android cloud phone through ADB, including taps, swipes, text input, and navigation that may change device state.

Mitigation: Use it only on devices you own or are authorized to operate, and verify actions with screenshots or UI dumps before continuing.

Risk: Screenshots and UI hierarchy dumps may capture passwords, one-time codes, private messages, financial data, or account settings.

Mitigation: Avoid running it on sensitive screens unless necessary, and handle captured screenshots or dumps as sensitive data.

Risk: ADB action commands are fire-and-forget and may not report whether the intended UI state changed.

Mitigation: Take a screenshot or dump the UI hierarchy after each action before issuing the next command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duoplusofficial/skills/duoplus-agent)
- [DuoPlus Official Website](https://www.duoplus.net/)
- [Publisher Profile](https://clawhub.ai/user/duoplusofficial)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires adb, cwebp, and an authorized Android device running the DuoPlus CloudPhone service.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
