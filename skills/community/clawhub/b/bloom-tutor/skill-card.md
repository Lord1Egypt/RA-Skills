## Description:

Bloom Tutor guides Chinese-language, one-on-one Socratic learning by creating adaptive course documents, collecting learner feedback, tracking progress, and generating course summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-evan](https://clawhub.ai/user/li-evan)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and educators use this skill to run Chinese-language study sessions where an agent creates a course folder, syllabus, sequential lesson articles, feedback-aware follow-up lessons, learning logs, and a final summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broadly from workspace Markdown files and learning-log.jsonl to adapt lessons and summarize progress.

Mitigation: Use a dedicated workspace or course folder, and keep unrelated private Markdown outside the workspace root.

Risk: The skill persists learning notes and progress locally, including an intermediate pre-summary.md file that is not discussed with the user during normal tutoring.

Mitigation: Review generated course folders and logs before sharing the workspace or installing the skill in a sensitive environment.

## Reference(s):

- [Bloom Tutor ClawHub Page](https://clawhub.ai/li-evan/skills/bloom-tutor)
- [Course Article Format and Tutor Principles](references/articles.md)
- [Learning Log and Progressive Loading](references/logging.md)
- [Summary Material Collection and Course Completion](references/summary.md)
- [Course Syllabus Rules](references/syllabus.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, JSON, Guidance]

**Output Format:** [Chinese-language Markdown lesson files, syllabus and summary files, JSONL learning-log entries, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists learning notes and progress in workspace files, including course folders, syllabus.md, numbered lesson Markdown files, summary.md, and learning-log.jsonl.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
