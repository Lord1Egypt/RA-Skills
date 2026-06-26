## Description: <br>
Programmatically control Claude Code in visible macOS Terminal windows via AppleScript for command input, screenshots, session logging, and terminal management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melichar-m](https://clawhub.ai/user/melichar-m) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to automate Claude Code sessions in macOS Terminal.app, including launching a project, sending tasks, capturing screenshots, and saving session logs for review or testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad terminal and screen-control power through macOS automation. <br>
Mitigation: Install and run it only in trusted project directories with Terminal.app and Script Editor permissions intentionally granted. <br>
Risk: Weak safeguards around command injection and trust approvals can make untrusted paths or long command text risky. <br>
Mitigation: Avoid passing untrusted project paths or command text, and review task text and approval flows before execution. <br>
Risk: Screenshots and saved session logs may capture secrets, customer data, or private repository content. <br>
Mitigation: Keep sensitive terminals out of view, avoid sessions that display secrets, and review or disable saved recordings for private work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/melichar-m/claude-code-control) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Package Metadata](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [JavaScript API results, JSON session recordings, screenshot file paths, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Node.js 18 or newer, Claude Code authentication, and Accessibility permissions for Terminal.app and Script Editor.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
