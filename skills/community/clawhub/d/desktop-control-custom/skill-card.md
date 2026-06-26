## Description: <br>
Advanced desktop automation with mouse, keyboard, screen capture, window management, clipboard, and image-recognition controls for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an OpenClaw agent automate local desktop workflows through mouse movement, keyboard input, screenshots, window control, clipboard access, and higher-level task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over the active desktop, including mouse, keyboard, clipboard, screenshots, app launches, and window operations. <br>
Mitigation: Install only when this level of local desktop control is intended, keep failsafe enabled, and use approval mode where possible. <br>
Risk: Desktop automation can expose passwords, private documents, chats, admin tools, or sensitive clipboard data if it runs in the wrong context. <br>
Mitigation: Avoid running it while sensitive information is visible or present in the clipboard, and manually review form submissions, file modifications, app launches, and public posts before they happen. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexbingquanxu-cpu/desktop-control-custom) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [AI agent guide](artifact/AI_AGENT_GUIDE.md) <br>
- [Quick reference](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown documentation with Python examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local desktop actions, screenshots, clipboard reads and writes, logs, and Python return values when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
