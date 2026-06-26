## Description: <br>
Chronos is a universal recurring-task manager that supports multiple schedule types, monthly quotas, automatic cron reminders, and a unified todo view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mathlife](https://clawhub.ai/user/mathlife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Chronos to manage local recurring tasks, scheduled one-time work, overdue completion, and reminder delivery through a shared todo database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chronos can modify local task data in todo.db. <br>
Mitigation: Back up todo.db before running maintenance commands with --apply, and review dry-run output before applying migrations or cleanup. <br>
Risk: Chronos can create or remove cron reminders and send todo content to a configured chat. <br>
Mitigation: Configure CHRONOS_CHAT_ID intentionally and treat todo snapshots and reminder payloads as potentially sensitive. <br>
Risk: Optional meta-review and subagent-memory handlers read and update workspace files and helper-script state. <br>
Mitigation: Enable those handlers only in trusted workspaces where the files and helper scripts they access are expected. <br>


## Reference(s): <br>
- [Chronos on ClawHub](https://clawhub.ai/mathlife/chronos) <br>
- [Publisher profile](https://clawhub.ai/user/mathlife) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local todo.db state, cron reminders, and task metadata when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.6.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
