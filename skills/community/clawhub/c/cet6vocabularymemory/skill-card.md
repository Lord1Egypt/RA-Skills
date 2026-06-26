## Description: <br>
基于艾宾浩斯遗忘曲线的英语六级词汇记忆系统，支持新单词学习与测验、智能复习计划、定时任务提醒和学习进度追踪，适用于中国大学生备考CET-6。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangrammer](https://clawhub.ai/user/gangrammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and agents use this skill to guide CET-6 vocabulary study with spaced repetition, quizzes, review scheduling, and progress tracking. It is aimed at Chinese university students preparing for the College English Test Band 6. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder setup can create persistent cron jobs and send automated messages. <br>
Mitigation: Confirm the cron schedule, script path, OpenClaw account, and recipient target before enabling reminders. <br>
Risk: The reminder behavior lacks complete cleanup and script provenance guidance. <br>
Mitigation: Document how to remove installed cron entries and delete the schedule and progress CSV files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangrammer/cet6vocabularymemory) <br>
- [CET-6 vocabulary list](references/cet6-vocabulary.md) <br>
- [Memory algorithm and review plan](references/memory-algorithm.md) <br>
- [Schedule configuration](references/schedule-config.md) <br>
- [CSV schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown study prompts with quiz content, scheduling guidance, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to CSV files for user schedule and word memory status tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
