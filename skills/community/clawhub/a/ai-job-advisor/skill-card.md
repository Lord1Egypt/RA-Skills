## Description:

AI job advisor that helps analyze roles, tailor resumes, prepare for interviews, draft HR follow-ups, negotiate offers, and manage job-search progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzhukai-png](https://clawhub.ai/user/iamzhukai-png)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to analyze job descriptions, tailor resumes, prepare for interviews, draft follow-up messages, compare offers, and keep job-search progress records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save sensitive job-search details.

Mitigation: Disable or modify auto-save behavior before use, and store only the job-search records the user explicitly wants retained.

Risk: The skill may read prior local job-search records without clear permission.

Mitigation: Limit access to explicitly selected files and avoid allowing the skill to inspect old Downloads records unless the user chooses them.

Risk: Screenshots of chats, offers, job descriptions, or resumes may contain personal or confidential information.

Mitigation: Redact screenshots and resume content before upload or processing.

Risk: Generated resumes may include remote scripts, remote fonts, or hardcoded branding from the bundled HTML template.

Mitigation: Remove remote script or font dependencies and hardcoded branding before sharing generated resumes externally.

## Reference(s):

- [Ai Job Advisor on ClawHub](https://clawhub.ai/iamzhukai-png/skills/ai-job-advisor)
- [Publisher profile](https://clawhub.ai/user/iamzhukai-png)
- [Bundled resume template](artifact/resume-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance, HTML resume templates, and generated local Markdown or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local job-search memory records and resume files as part of the skill workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
