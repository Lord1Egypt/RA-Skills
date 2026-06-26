## Description: <br>
Interact with DingTalk enterprise workspace using the dws CLI to search contacts and departments, send chat messages, manage calendar events and meeting rooms, create and manage todos, handle approvals, review attendance records, manage reports, and work with AITable data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhu888](https://clawhub.ai/user/brucezhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, workspace administrators, and developers use this skill to operate DingTalk workplace functions through the dws CLI, including contact lookup, messaging, calendar scheduling, todos, approvals, attendance, reports, and AITable workflows. It is intended for authenticated DingTalk environments where the agent has explicit authorization to access or change workspace data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands and helper scripts can change live workplace data, including approvals, chat messages, todos, calendar events, and AITable records. <br>
Mitigation: Use a least-privileged DingTalk app, test in a sandbox tenant, run mutation commands with --dry-run first, and require human confirmation before execution. <br>
Risk: Contact, attendance, report, and department-member workflows can expose employee information such as mobile numbers, attendance records, senders, and user IDs. <br>
Mitigation: Only retrieve or export employee data for authorized business needs, limit returned fields with --jq or --fields, and avoid broad exports unless approved. <br>
Risk: The skill requires DingTalk OAuth credentials and documents installer-based CLI setup. <br>
Mitigation: Review installer scripts before running them, prefer verified releases or source builds, store credentials in the system keychain where possible, and avoid exposing environment variables in logs. <br>


## Reference(s): <br>
- [Dingtalk Workspace on ClawHub](https://clawhub.ai/brucezhu888/dingtalk-workspace) <br>
- [DingTalk Workspace CLI Repository](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) <br>
- [DingTalk Workspace CLI Releases](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases) <br>
- [DingTalk Open Platform Console](https://open-dev.dingtalk.com/fe/app) <br>
- [Global Reference](references/global-reference.md) <br>
- [Intent Guide](references/intent-guide.md) <br>
- [Error Codes Reference](references/error-codes.md) <br>
- [Calendar Reference](references/products/calendar.md) <br>
- [Approval Reference](references/products/oa.md) <br>
- [Attendance Reference](references/products/attendance.md) <br>
- [AITable Reference](references/products/aitable.md) <br>
- [Chat Reference](references/products/chat.md) <br>
- [Contact Reference](references/products/contact.md) <br>
- [Report Reference](references/products/report.md) <br>
- [Todo Reference](references/products/todo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python helper script guidance, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent output usually consists of dws CLI commands, setup guidance, filtered JSON examples, and safe-execution steps such as dry-run previews and human confirmation before mutations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence and clawhub.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
