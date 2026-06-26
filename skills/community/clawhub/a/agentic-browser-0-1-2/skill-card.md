## Description: <br>
Browser automation for AI agents via inference.sh, including navigation, element interaction with @e refs, screenshots, video recording, form automation, file upload, and JavaScript execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyny89](https://clawhub.ai/user/xyny89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-focused agents use this skill to drive browser sessions for web automation, data extraction, testing, research, authenticated workflows, screenshots, and recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over browser sessions, including login, form submission, upload, JavaScript execution, screenshots, recordings, and proxy use. <br>
Mitigation: Use only on sites and accounts the operator is authorized to automate, and require explicit approval before sensitive browser actions. <br>
Risk: Browser sessions can involve cookies, authenticated state, uploaded files, screenshots, recordings, and proxy credentials. <br>
Mitigation: Avoid exporting cookies, approve recording and proxy use before execution, limit uploaded files to intended paths, and close sessions promptly after each task. <br>


## Reference(s): <br>
- [Agentic Browser on ClawHub](https://clawhub.ai/xyny89/agentic-browser-0-1-2) <br>
- [Command Reference](references/commands.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Session Management](references/session-management.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [inference.sh Sessions](https://inference.sh/docs/extend/sessions) <br>
- [inference.sh Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON inputs, and generated browser artifacts such as screenshots or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser sessions may return compact element refs, screenshots, session identifiers, and video files depending on the requested action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
