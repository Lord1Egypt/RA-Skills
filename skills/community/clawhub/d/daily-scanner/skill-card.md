## Description: <br>
每日Get笔记智能盘点 scans recent Get笔记 recordings, classifies them, processes useful items, updates CRM-related records, and produces a daily report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skychentian](https://clawhub.ai/user/skychentian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or operators use this skill to scan the last 24 hours of Get笔记 recordings, classify business-relevant notes, route them to related workflows, and summarize follow-up work. It is aimed at daily review of customer communications, meetings, channel activity, investment notes, ideas, and content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan private recordings from the user's Get笔记 folder. <br>
Mitigation: Install only when that folder is intended for agent review, and define retention or deletion rules for scanned recordings and derived summaries. <br>
Risk: The skill can change CRM, task, channel, and related library systems without enough explicit approval controls. <br>
Mitigation: Run in report-only or manual-review mode until external writes require explicit approval and use least-privilege credentials. <br>
Risk: Broad trigger phrases and scheduled execution can cause unintended scans or updates. <br>
Mitigation: Use narrow trigger phrases and require opt-in scheduler controls before enabling daily or midnight automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skychentian/daily-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/skychentian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily summary report with classification counts, CRM update details, to-dos, priority reminders, and a short completion summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate updates to Feishu CRM, TickTick, channel tables, and related libraries when the connected agent environment permits those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
