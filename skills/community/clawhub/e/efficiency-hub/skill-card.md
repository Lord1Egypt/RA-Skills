## Description:

效率中枢 - 一站式日常任务处理中心。整合搜索、保存、提醒、计划、复盘等日常高频需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a Chinese-language productivity hub for everyday search, saving, reminders, planning, and recap workflows. It helps an agent interpret broad requests and route them into practical task handling steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save chat content, search memory, create reminders, back up files, use web search, and delegate to other skills without clear confirmation boundaries.

Mitigation: Require explicit user confirmation before writes, searches, reminder creation, backups, web access, or delegation.

Risk: Broad triggers such as busy or convenience requests may activate workflows the user did not intend.

Mitigation: Use narrow triggers, preview the intended action, and ask the user to confirm before executing side effects.

Risk: Saved content, backups, and scheduled reminders may persist longer than the user expects.

Mitigation: Apply path limits, retention and deletion controls, and provide a way to list or cancel scheduled reminders.

## Reference(s):

- [快速命令库](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/xhmqq616/skills/efficiency-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with task-specific command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose saving content, searching memory or the web, scheduling reminders, backing up files, and delegating to other skills when the user confirms those actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
