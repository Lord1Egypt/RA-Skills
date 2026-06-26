## Description: <br>
DingTalk CLI Auto helps agents automate DingTalk messaging, calendar, todo, contact lookup, and group robot workflows through the dws CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to automate DingTalk workplace workflows, including sending messages, managing meetings, assigning todos, searching contacts, and posting group robot notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill wraps dws command execution in a shell command string, which can be unsafe when arguments contain untrusted content. <br>
Mitigation: Review or patch the wrapper to use argument-array process spawning before using real DingTalk credentials. <br>
Risk: The skill can access DingTalk credentials, calendar data, todos, and contact information. <br>
Mitigation: Use least-privilege DingTalk application permissions, avoid pasting secrets into commands, and start with a test tenant or non-production account. <br>
Risk: Calendar and todo delete operations can change or remove workplace records. <br>
Mitigation: Require explicit confirmation before deletion or completion commands and verify record IDs before execution. <br>
Risk: Bulk contact lookup can expose personal or organizational directory data. <br>
Mitigation: Limit contact queries to the minimum needed and avoid printing or retaining unnecessary contact details. <br>
Risk: The dws binary is an external dependency used to perform DingTalk actions. <br>
Mitigation: Verify the dws binary source and version before installing or executing the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onlyloveher/dingtalk-cli-auto) <br>
- [DingTalk Workspace CLI](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and DingTalk operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the dws CLI, DingTalk application credentials, and OAuth authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
