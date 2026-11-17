## Description:

AI screen vision and desktop control skill for OpenClaw that uses screenshot analysis to understand UI elements and perform mouse and keyboard actions across Linux, macOS, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guitu917](https://clawhub.ai/user/guitu917)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent inspect the current desktop, reason about visible UI state, and execute bounded GUI tasks such as clicking, typing, scrolling, form filling, web browsing, and screenshot capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can view and operate the user's desktop, so screenshots and actions may expose credentials, private documents, financial accounts, or authenticated business tools.

Mitigation: Run only in a disposable or tightly controlled environment and avoid use on sensitive screens unless the configured vision provider and network exposure are fully trusted.

Risk: The server security summary flags unsafe safeguards and headless remote-desktop setup for a tool that can see and operate the screen.

Mitigation: Review VNC password and listener configuration, endpoint validation, confirmation enforcement, screenshot logging, and installer secret handling before deployment.

Risk: Screenshots are logged by default, creating persistent records of visible desktop content.

Mitigation: Disable or tightly restrict screenshot logging, protect log storage, and clear logs after task completion when screen contents may be sensitive.

## Reference(s):

- [Platform Setup Guide](references/PLATFORM_GUIDE.md)
- [Vision API Configuration](references/API_CONFIG.md)
- [Usage Examples](references/EXAMPLES.md)
- [ClawHub Skill Page](https://clawhub.ai/guitu917/skills/ai-screen-vision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured task results, action histories, screenshot paths, and setup or configuration guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
