## Description:

基于艾宾浩斯遗忘曲线的英语四级词汇记忆系统，支持新单词学习与测验、智能复习计划、定时提醒和学习进度追踪，适用于中国大学生备考 CET-4。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangrammer](https://clawhub.ai/user/gangrammer)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and education-focused agents use this skill to guide CET-4 vocabulary study with scheduled learning, quizzes, spaced review, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder setup may modify persistent crontab entries.

Mitigation: Require explicit user approval for the exact schedule, command, and removal method before any cron change; prefer an app-scoped reminder mechanism.

Risk: Reminder commands may send outbound messages from a default account.

Mitigation: Require explicit approval of the account, recipient, and message content before sending or scheduling reminders.

Risk: Reminder examples reference scripts under /root.

Mitigation: Avoid privileged paths unless the user has reviewed and approved the exact script location and execution context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gangrammer/skills/cet4vocabularymemory)
- [复习计划与记忆算法](references/memory-algorithm.md)
- [数据库表结构](references/schema.md)
- [定时任务配置](references/schedule-config.md)
- [大学英语四级词汇表 (CET-4) 完整版](references/cet4-vocabulary.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with vocabulary tables, quiz prompts, CSV state updates, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent reminder configuration and updates to local CSV study-state files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
