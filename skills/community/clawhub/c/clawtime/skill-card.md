## Description: <br>
Operate ClawTime - webchat widgets, task panel, and avatar creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngkent](https://clawhub.ai/user/youngkent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill as an operational reference for ClawTime, including webchat widget markup, task panel conventions, and Three.js avatar creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references local files that may contain secrets or active session data. <br>
Mitigation: Treat ~/.clawtime/.env, credentials.json, and sessions.json as secrets and do not ask an agent to read or summarize them unless intentionally managing credentials. <br>
Risk: Custom avatar JavaScript can execute behavior beyond static documentation examples. <br>
Mitigation: Review custom avatar JavaScript before using it. <br>
Risk: The persistent task list may expose private work details. <br>
Mitigation: Avoid putting private information into ~/.clawtime/tasks.json. <br>
Risk: The referenced INSTALL.md is not included in the artifact evidence. <br>
Mitigation: Review the missing INSTALL.md separately before relying on installation, configuration, or troubleshooting steps. <br>


## Reference(s): <br>
- [ClawTime release page](https://clawhub.ai/youngkent/clawtime) <br>
- [Publisher profile](https://clawhub.ai/user/youngkent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawTime widget markup and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
