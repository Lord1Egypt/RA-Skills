## Description: <br>
基于艾宾浩斯遗忘曲线的英语四级词汇记忆系统，支持新单词学习、测验、智能复习计划、定时提醒和学习进度追踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangrammer](https://clawhub.ai/user/gangrammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CET-4 learners use this skill to study new English vocabulary, take quizzes, schedule spaced reviews, and track local progress while preparing for China's College English Test Band 4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring reminders can create persistent local scheduled jobs or target the wrong OpenClaw account or user. <br>
Mitigation: Confirm the exact crontab entries, OpenClaw account, target user, and removal steps before enabling reminders. <br>
Risk: Local study tracking may store user identifiers, study times, and word-memory progress in CSV files. <br>
Mitigation: Keep the CSV files local, avoid unnecessary personal data, and review the files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangrammer/cet4vocabularymemory) <br>
- [CET-4 vocabulary list](references/cet4-vocabulary.md) <br>
- [Memory algorithm and review schedule](references/memory-algorithm.md) <br>
- [Schedule configuration](references/schedule-config.md) <br>
- [Data schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with study prompts, quiz flows, CSV tracking updates, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV files for schedule and word-memory status; reminder configuration should be reviewed before enabling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
