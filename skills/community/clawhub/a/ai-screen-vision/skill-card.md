## Description: <br>
Screen Vision lets an OpenClaw agent inspect screenshots, analyze desktop UI state with an OpenAI-compatible vision API, and perform mouse and keyboard actions in a controlled loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guitu917](https://clawhub.ai/user/guitu917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to let an agent view a desktop, understand UI elements, and carry out GUI tasks such as opening applications, browsing websites, filling forms, taking screenshots, and operating files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view and operate a live desktop, including mouse and keyboard control. <br>
Mitigation: Install and run it only in an isolated desktop or VM, and avoid using it with sensitive accounts, private screens, payment sessions, or production systems. <br>
Risk: Default remote desktop setup and screenshot logging can expose screen contents. <br>
Mitigation: Change or disable the VNC setup before use and disable screenshot logging when persistent logs are not needed. <br>
Risk: The advertised confirmation safeguards may not be sufficient for destructive or financial actions. <br>
Mitigation: Require manual review outside the skill before any destructive, privileged, purchase, payment, or transfer action. <br>
Risk: Screenshots and task context may be sent to a configured vision provider. <br>
Mitigation: Use a local or otherwise trusted vision provider and verify API endpoint, model, and credential settings before running tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guitu917/ai-screen-vision) <br>
- [API Configuration](references/API_CONFIG.md) <br>
- [Platform Setup Guide](references/PLATFORM_GUIDE.md) <br>
- [Usage Examples](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration snippets, and shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce desktop automation actions, screenshots, logs, and vision API requests during use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and README badge) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
