## Description: <br>
Control the user's real Safari browser on macOS using AppleScript and screencapture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SDLLL](https://clawhub.ai/user/SDLLL) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an AI agent inspect, navigate, screenshot, and interact with their real Safari browser session on macOS. It is useful for browser tasks that need access to existing tabs, logged-in state, or Safari-specific behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a live logged-in Safari session, including open tabs, cookies, account pages, page contents, and screenshots. <br>
Mitigation: Install only when real Safari control is intended; close sensitive tabs and prefer a separate browser profile or test account before use. <br>
Risk: The artifacts do not show strong scoping or consent boundaries for reading pages, taking screenshots, interacting with accounts, or running JavaScript on pages. <br>
Mitigation: Require explicit confirmation before page reads, screenshots, account interactions, form submissions, or JavaScript execution. <br>
Risk: Foreground screenshot and keyboard automation can briefly activate Safari or type into the focused interface. <br>
Mitigation: Confirm Safari is frontmost and the intended tab or field is selected before using keyboard input or foreground screenshot workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SDLLL/claude-for-safari) <br>
- [Project website](https://safari.skilljam.dev) <br>
- [Project repository](https://github.com/SDLLL/claude-for-safari) <br>
- [Issue tracker](https://github.com/SDLLL/claude-for-safari/issues) <br>
- [macOS reference](https://www.apple.com/macos/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with AppleScript, JavaScript, shell commands, and concise operating guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and guidance for macOS Safari automation, including page reads, screenshots, navigation, clicks, form entry, scrolling, and tab switching.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
