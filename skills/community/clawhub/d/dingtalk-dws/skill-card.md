## Description: <br>
DingTalk CLI Skill helps an agent operate DingTalk workplace products through the dws CLI, including AI tables, calendars, contacts, chat bots, todos, approvals, attendance, reports, DING messages, and workbench tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cizixiu](https://clawhub.ai/user/cizixiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workplace automation users use this skill to route DingTalk requests to dws CLI commands, inspect workplace data, create or update tasks, schedule calendar activity, send bot or DING messages, and work with reports, attendance, contacts, and AI tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates workplace actions to an external dws CLI and requires OAuth credentials. <br>
Mitigation: Install only from a trusted source, verify the published checksum, and protect DWS_CLIENT_SECRET, webhook tokens, and DWS_CONFIG_DIR. <br>
Risk: The skill can read and modify sensitive DingTalk workplace data, including contacts, attendance, reports, tasks, calendars, and AI table records. <br>
Mitigation: Use least-privileged DingTalk credentials and review requested data access before allowing the agent to run commands. <br>
Risk: Some commands can delete records, change calendars, approve or reject workflows, send broad messages, or trigger paid DING SMS and calls. <br>
Mitigation: Require explicit human confirmation before destructive, approval, broad messaging, report distribution, attendance/contact lookup, calendar change, or paid notification actions. <br>
Risk: DWS_SERVERS_URL can alter service discovery behavior. <br>
Mitigation: Keep DWS_SERVERS_URL pinned to a trusted endpoint and review configuration changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cizixiu/dingtalk-dws) <br>
- [dws CLI latest release](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/latest) <br>
- [dws Windows CLI package](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases/download/v1.0.8/dws-windows-amd64.zip) <br>
- [Global reference](artifact/references/global-reference.md) <br>
- [Intent guide](artifact/references/intent-guide.md) <br>
- [Recovery guide](artifact/references/recovery-guide.md) <br>
- [AI table command reference](artifact/references/products/aitable.md) <br>
- [Calendar command reference](artifact/references/products/calendar.md) <br>
- [Chat and bot command reference](artifact/references/products/chat.md) <br>
- [DING message command reference](artifact/references/products/ding.md) <br>
- [Todo command reference](artifact/references/products/todo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-oriented CLI usage, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dws CLI plus DingTalk OAuth credentials or DWS environment variables; commands commonly return JSON when --format json is used.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact frontmatter reports 1.0.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
