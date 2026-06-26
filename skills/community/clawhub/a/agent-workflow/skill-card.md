## Description: <br>
A structured workflow plugin for OpenClaw agents that guides work through brainstorm, plan, execute, verify, and deliver steps with persistent state and multi-project support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangyishuai](https://clawhub.ai/user/kangyishuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this plugin to run explicit structured workflows for project planning, execution, review, and delivery in OpenClaw. It is intended for tasks where workflow state, branching, verification, and multi-project tracking help coordinate longer-running work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow state is stored locally under the OpenClaw workspace. <br>
Mitigation: Review the configured storage location before installation and avoid placing sensitive project details in workflow notes or outputs unless local storage is appropriate. <br>
Risk: Cleanup or discard prompts may delete workflow artifacts. <br>
Mitigation: Approve deletion only when the listed files are clearly temporary workflow artifacts and not user-created deliverables. <br>
Risk: Subagent delegation can expose unnecessary private context. <br>
Mitigation: Share only the context each subagent needs and avoid forwarding secrets, credentials, or unrelated private project details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kangyishuai/agent-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/kangyishuai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON tool responses with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores workflow state locally under the OpenClaw workspace and returns structured status, progress, warnings, and next-step guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
