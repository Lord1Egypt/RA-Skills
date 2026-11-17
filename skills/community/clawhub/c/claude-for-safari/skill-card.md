## Description:

Control the user's real Safari browser on macOS using AppleScript and screencapture for browsing, page reading, screenshots, navigation, clicking, form filling, scrolling, and tab management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdlll](https://clawhub.ai/user/sdlll)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users on macOS use this skill to let an agent inspect and operate their real Safari browser session for web research, page interaction, form entry, screenshots, and tab workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over a real logged-in Safari session, including cookies, open tabs, and authenticated pages.

Mitigation: Use narrow per-action approvals, avoid sensitive sites such as banking, admin, healthcare, and other high-risk accounts, and run it only in browser sessions intended for agent access.

Risk: The security evidence flags unsafe temporary-file execution in the screenshot helper path.

Mitigation: Review or pin the exact source before installation and repair the /tmp screenshot-helper commands before routine use.

Risk: Screenshots and AppleScript automation may expose page contents and require macOS privacy permissions.

Mitigation: Grant Automation and Screen Recording only to trusted terminal applications and revoke permissions when the skill is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdlll/skills/claude-for-safari)
- [Project website](https://safari.skilljam.dev)
- [Apple macOS](https://www.apple.com/macos/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with AppleScript, JavaScript, Swift, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS Safari and may require Automation, JavaScript from Apple Events, and Screen Recording permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
