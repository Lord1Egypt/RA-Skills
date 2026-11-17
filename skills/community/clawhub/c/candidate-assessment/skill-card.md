## Description:

Evaluates a candidate's resume against a job description and produces a structured fit assessment plus a professional hiring report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and recruiting operations teams use this skill to compare a candidate's resume with a target job description, score fit across a weighted hiring model, and generate interview-ready assessment artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned third-party package install path for PDF/DOCX processing.

Mitigation: Review before installing, run the skill in a contained environment, and avoid PDF/DOCX input unless pdfmuse has been installed from a vetted pinned version.

Risk: The skill handles resumes, job descriptions, intermediate extracts, and generated assessments that may contain sensitive hiring data.

Mitigation: Use it only for candidate and job materials you are authorized to process, and delete intermediate resume/JD extracts and assessment reports when no longer needed.

## Reference(s):

- [ClawHub Candidate Assessment skill page](https://clawhub.ai/casperkwok/skills/candidate-assessment)
- [Assessment prompt and JSON schema](artifact/reference/assessment-prompt.md)
- [Report design reference](artifact/reference/report-design.md)
- [resume-parsing dependency](https://github.com/casperkwok/resume-parsing-skill)
- [pdfmuse package](https://pypi.org/project/pdfmuse/)
- [pdfmuse source repository](https://github.com/casperkwok/pdfmuse)

## Skill Output:

**Output Type(s):** [text, json, html, pdf, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON, HTML, and optional PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; PDF/DOCX JD handling may install pdfmuse, and optional PDF export requires Chrome, Chromium, or Edge.]

## Skill Version(s):

1.0.3 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
