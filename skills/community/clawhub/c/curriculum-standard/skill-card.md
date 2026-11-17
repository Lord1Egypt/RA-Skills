## Description:

Generates DOCX course-standard documents from talent training plans and professional teaching standards for Chinese vocational education.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Vocational education curriculum designers, instructors, and school staff use this skill to create structured Chinese course-standard documents with course objectives, learning scenarios, academic quality levels, implementation guidance, and assessment standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive school, student, or institutional documents may be processed by the skill.

Mitigation: Review the skill before installing, use approved document-handling procedures, and remove or redact sensitive inputs when possible.

Risk: Intermediate files and logs may be retained after generation.

Mitigation: Define cleanup and retention rules before use, and prefer prompting before retaining debug artifacts.

Risk: Remote PDF downloading is under-scoped.

Mitigation: Restrict downloads to verified official sources and enforce file size and content-type checks.

## Reference(s):

- [Server-resolved source repository](https://github.com/flyboat403/curriculum-standard)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/curriculum-standard)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [DOCX course-standard document, with Markdown fallback guidance when DOCX conversion fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a ten-section Chinese vocational education course standard from user-provided training plans and optional teaching standards, templates, and content references.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
