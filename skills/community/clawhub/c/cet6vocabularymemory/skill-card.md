## Description:

基于艾宾浩斯遗忘曲线的英语六级词汇记忆系统，支持新单词学习与测验、智能复习计划、定时任务提醒和学习进度追踪，适用于中国大学生备考CET-6。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangrammer](https://clawhub.ai/user/gangrammer)

### License/Terms of Use:

MIT-0

## Use Case:

Students preparing for China's CET-6 English exam use this skill to learn vocabulary, schedule spaced reviews, take spelling, choice, and translation quizzes, and track mastery over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder setup may create persistent cron jobs that call an unaudited root-path CET-4 reminder script and send messages through a default account.

Mitigation: Require explicit confirmation before any cron change, verify or replace the referenced reminder script, and avoid root-owned paths and default messaging accounts.

Risk: Schedule and progress CSV files can retain user identifiers, learning schedules, and memory state without clear lifecycle controls.

Mitigation: Provide a clear way to list, disable, and delete stored schedule data, progress records, and reminders.

## Reference(s):

- [CET-6 vocabulary list](references/cet6-vocabulary.md)
- [Memory algorithm and review plan](references/memory-algorithm.md)
- [Schedule configuration](references/schedule-config.md)
- [CSV schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversational guidance with vocabulary prompts, quiz items, CSV status updates, and optional cron shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent reminder configuration and local CSV updates for schedule and memory state.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
