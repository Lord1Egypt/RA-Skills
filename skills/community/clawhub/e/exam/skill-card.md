## Description:

Generate practice tests, flashcards, study schedules, and timed simulations from any study material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Students, certification candidates, and professionals use this skill to turn study materials into practice questions, flashcards, timed mock exams, study schedules, and progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep study questions, flashcards, session history, and performance statistics locally under ~/exams/.

Mitigation: Avoid sensitive notes or proprietary exam materials unless local storage is acceptable, and review or remove stored study files when no longer needed.

Risk: Study reminders may create scheduled cron jobs.

Mitigation: Review the exact scheduled job before enabling reminders and confirm how to remove it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured study artifacts and optional JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local study files and reminder setup guidance when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
