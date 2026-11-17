## Description: <br>
Provides an agent with mouse and keyboard control, screenshots, window activation, clipboard actions, and failsafe guidance for local desktop automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to have an agent generate and run local desktop automation for repetitive form entry, window operations, screenshots, clipboard transfer, and cross-application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated clicking and typing can affect the wrong window or submit unintended changes. <br>
Mitigation: Verify the active window before actions and require user confirmation before submissions or other irreversible operations. <br>
Risk: Screenshots and clipboard access can expose sensitive on-screen or copied information. <br>
Mitigation: Limit screenshot regions, avoid clipboard use for secrets, and review captured or copied content before sharing it. <br>
Risk: Desktop automation can continue after user intent changes if emergency stop behavior is not preserved. <br>
Mitigation: Keep failsafe enabled and move the pointer to a screen corner to stop automation when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/desktop-automation-hub-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce executable desktop-automation steps that control mouse, keyboard, windows, screenshots, and clipboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
