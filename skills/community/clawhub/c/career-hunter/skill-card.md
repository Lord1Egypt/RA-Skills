## Description:

Job search assistant that generates and polishes resumes, writes cover letters, tracks applications, prepares for interviews, and searches for jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage job searches, including resume and cover-letter drafting, application tracking, interview preparation, and finding current job openings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store job-search records and generated application materials on disk.

Mitigation: Review or delete ~/.openclaw/job-tracker.json, resume.md, and cover-letter files when they are no longer needed, especially on shared machines.

Risk: Generated resumes, cover letters, interview answers, or job-search results may contain incorrect or overstated information.

Mitigation: Review generated materials before use and verify that they only include experience and achievements the user provided.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanthienha199/skills/career-hunter)
- [Publisher profile](https://clawhub.ai/user/vanthienha199)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Markdown, JSON, and plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local resume, cover letter, and application tracker files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
