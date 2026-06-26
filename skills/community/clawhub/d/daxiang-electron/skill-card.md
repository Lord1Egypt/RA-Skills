## Description: <br>
Automates Electron desktop apps such as VS Code, Slack, Discord, Figma, Notion, and Spotify through agent-browser over Chrome DevTools Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to local Electron applications, inspect UI state, interact with windows or webviews, fill forms, extract visible data, and capture screenshots for automation or testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote debugging can give the agent broad control over local Electron apps and access to visible app data. <br>
Mitigation: Enable CDP only for the specific app and task the user approves, then close the debug-enabled app session when the task is complete. <br>
Risk: Screenshots and data extraction can expose sensitive content from chats, developer tools, workspaces, password managers, or production accounts. <br>
Mitigation: Avoid sensitive apps or accounts unless the user explicitly approves the exact app and action, and review screenshot or extraction steps before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daxiangnaoyang/daxiang-electron) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to produce screenshots, JSON snapshots, or extracted text when agent-browser commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
