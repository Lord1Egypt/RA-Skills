## Description: <br>
Automates macOS browser and desktop workflows through screenshot review, browser actions, keyboard and mouse control, file operations, and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinxulin8899-dotcom](https://clawhub.ai/user/jinxulin8899-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent perform supervised macOS tasks that span web pages, desktop dialogs, files, downloads, and application input. It is suited to multi-step desktop automation where the agent must observe the screen, act, and verify progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over the screen, keyboard, clipboard, browser, files, downloads, and shell commands. <br>
Mitigation: Install only for intentional supervised desktop-control use, and review shell commands, file moves, downloads, login or form actions, and messages before allowing them. <br>
Risk: The security evidence says built-in safety gates are not sufficient for sensitive use. <br>
Mitigation: Avoid using it with secrets or sensitive applications unless confirmations, shell and file constraints, clipboard handling, and screenshot cleanup are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinxulin8899-dotcom/chuntai-desktop-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, clipboard actions, desktop input events, shell command output, and status updates during supervised execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
