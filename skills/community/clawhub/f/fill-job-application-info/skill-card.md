## Description:

将用户提供的简历文本或简历文件（PDF、DOCX、DOC、TXT、Markdown，以及常见表格导出）整理成结构化候选人资料，再将这些信息填写到招聘报名表、应聘登记表、招聘网站或 ATS 招聘系统中。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkpeace](https://clawhub.ai/user/thinkpeace)

### License/Terms of Use:

MIT-0

## Use Case:

Job applicants and recruiting support users use this skill to turn resume text or resume files into structured candidate profiles, then fill job application forms, registration files, recruiting websites, or ATS systems. It emphasizes preserving original candidate data, asking for clarification when fields are missing or ambiguous, and pausing before final submission unless the user explicitly approves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and application workflows may involve sensitive fields such as identity numbers, demographic details, family information, and attachments.

Mitigation: Review sensitive fields and attachments before any upload or submission, and keep the pause-before-submit behavior enabled for irreversible actions.

Risk: Missing or ambiguous candidate fields could result in inaccurate application data.

Mitigation: Preserve original values, mark unknown fields instead of inventing them, ask the user for clarification, and review mapped fields before submission.

## Reference(s):

- [Candidate Profile Schema](references/resume-profile-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/thinkpeace/skills/fill-job-application-info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Structured candidate data, filled application artifacts, and human-readable review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route work through PDF, DOCX, XLSX, or browser automation skills depending on the target form or website.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
