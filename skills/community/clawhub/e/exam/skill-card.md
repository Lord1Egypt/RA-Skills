## Description: <br>
Generate practice tests, flashcards, study schedules, and timed simulations from any study material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students, certification candidates, and professionals use this skill to turn study materials into practice questions, flashcards, timed mock exams, study schedules, summaries, and progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated questions, answers, flashcards, and performance history may be saved locally under ~/exams/. <br>
Mitigation: Review what is being saved and avoid storing sensitive study materials or answers on shared machines. <br>
Risk: Study reminders may add cron entries that continue after the exam date. <br>
Mitigation: Ask the agent to show the exact cron entry before enabling it and remove the entry when the exam is over. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/exam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with question sets, flashcards, study plans, progress reports, JSON or JSONL examples, and occasional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local study files under ~/exams/ and optional cron reminders for study scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
