## Description: <br>
Advanced desktop automation with mouse, keyboard, screen, window, and clipboard control for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpegley](https://clawhub.ai/user/wpegley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to automate live desktop workflows, including mouse movement, keyboard input, screenshots, image lookup, window control, clipboard operations, and higher-level desktop tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live desktop with broad mouse, keyboard, window, screenshot, and clipboard access. <br>
Mitigation: Install only when live desktop control is intended, keep failsafe enabled, and supervise workflows that affect applications or accounts. <br>
Risk: Automation can submit forms, change files, launch apps, save screenshots, or act through logged-in accounts. <br>
Mitigation: Use approval mode for important workflows, close sensitive windows, and review planned actions before execution. <br>
Risk: Screenshots and clipboard reads can expose private or sensitive information. <br>
Mitigation: Avoid clipboard reads unless necessary and clear or hide sensitive content before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wpegley/desktop-control-1-0-0) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [AI_AGENT_GUIDE.md](artifact/AI_AGENT_GUIDE.md) <br>
- [QUICK_REFERENCE.md](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown documentation with Python examples and optional screenshot or clipboard/file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be accompanied by live desktop actions, screenshots, logs, or clipboard changes depending on the invoked operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
