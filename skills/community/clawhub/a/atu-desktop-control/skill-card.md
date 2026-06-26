## Description: <br>
Full desktop automation for screenshots, mouse, keyboard, window management, clipboard, and screen information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoohsuan](https://clawhub.ai/user/qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent inspect and operate a live desktop through screenshots, mouse actions, keyboard input, window management, clipboard access, and screen queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over the live desktop, including screen capture, mouse movement, keyboard input, clipboard access, and window closing. <br>
Mitigation: Use it only when intentional desktop control is required, keep pyautogui failsafe enabled, and require explicit confirmation before screenshots, clipboard reads, keyboard shortcuts, or closing windows. <br>
Risk: Screenshots or clipboard reads can expose passwords, tokens, private chats, financial data, or sensitive documents visible on screen or in the clipboard. <br>
Mitigation: Close or hide sensitive content and clear sensitive clipboard data before running the skill. <br>
Risk: Window-management and keyboard actions can disrupt active work or close unsaved documents. <br>
Mitigation: Run commands in a controlled desktop session and review target windows or coordinates before executing destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qoohsuan/atu-desktop-control) <br>
- [OpenClaw](https://github.com/nichochar/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON command results, screenshot image files, and setup or usage commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return ok/error JSON; screenshots are saved locally under captures/ unless an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
