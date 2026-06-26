## Description: <br>
Control desktop apps via mouse and keyboard, capture screenshots, teach AI tasks by demonstration, and automate workflows with saved reusable tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent capture the desktop, issue mouse and keyboard actions, and record reusable desktop automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad unsandboxed control over the live screen, mouse, keyboard, screenshots, and saved task replay. <br>
Mitigation: Use it only when intentional and supervised; close sensitive applications before use. <br>
Risk: Screenshots and OCR can expose passwords, tokens, payments, private messages, or administrative settings visible on screen. <br>
Mitigation: Avoid teaching or replaying workflows involving sensitive data and remove private content from view before capture. <br>
Risk: Saved task JSON can replay desktop actions later without enough built-in safeguards. <br>
Mitigation: Review saved task JSON before running it and keep learned tasks scoped to low-risk workflows. <br>


## Reference(s): <br>
- [Desktop Agent ClawHub listing](https://clawhub.ai/fuzzyb33s/desktop-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot image files and learned task JSON files in the local workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
