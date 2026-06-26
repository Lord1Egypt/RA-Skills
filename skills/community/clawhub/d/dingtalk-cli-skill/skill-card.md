## Description: <br>
Dingtalk CLI SKILL helps an agent operate DingTalk workspace features through the dws CLI, including AI tables, calendars, contacts, group bots, todos, approvals, attendance, reports, DING messages, and workbench tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cizixiu](https://clawhub.ai/user/cizixiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workplace automation agents use this skill to query and manage DingTalk business data and workflows, including todos, schedules, contacts, attendance, reports, AI table records, attachments, and group bot messages. Developers can also use the bundled Python helper scripts as repeatable command wrappers around the dws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over DingTalk business data, messages, calendars, attendance, and credentials. <br>
Mitigation: Install it only for workspaces where agent-operated DingTalk automation is intended, and restrict who can invoke the skill. <br>
Risk: Credential and token exposure could allow unintended DingTalk access. <br>
Mitigation: Protect DWS_CLIENT_SECRET and webhook tokens, and avoid sharing logs that contain tokens or employee data. <br>
Risk: High-impact operations such as delete, message-send, attendance, calendar, or bulk table actions can affect other users or business records. <br>
Mitigation: Require explicit human confirmation before those operations are executed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cizixiu/dingtalk-cli-skill) <br>
- [DingTalk workspace CLI latest release](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest) <br>
- [dws Windows AMD64 package](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/download/v1.0.8/dws-windows-amd64.zip) <br>
- [Global reference](references/global-reference.md) <br>
- [Intent routing guide](references/intent-guide.md) <br>
- [Field rules](references/field-rules.md) <br>
- [Recovery guide](references/recovery-guide.md) <br>
- [AI table command reference](references/products/aitable.md) <br>
- [Calendar command reference](references/products/calendar.md) <br>
- [Contact command reference](references/products/contact.md) <br>
- [Todo command reference](references/products/todo.md) <br>
- [Attendance command reference](references/products/attendance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dws binary and DingTalk OAuth-related environment configuration before live workspace operations can run.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
