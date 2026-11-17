## Description:

Create professional Harvard-style resumes, CVs, and matching cover letters from user-provided candidate descriptions, structured data, or existing resumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasoncodespace](https://clawhub.ai/user/jasoncodespace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn candidate notes, structured profile data, or existing resumes into role-targeted resumes and optional matching cover letters. It supports one or more job tracks, stronger bullets, clean black-and-white formatting, and DOCX output with optional PDF conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume generation may process sensitive candidate personal data.

Mitigation: Install and run the skill in a constrained workspace, and provide only the personal data needed for the resume or cover letter.

Risk: Installing python-docx and transitive dependencies introduces supply-chain exposure.

Mitigation: Pin and review python-docx and its transitive dependencies before running the documented pip install step.

Risk: Role-targeted rewriting can accidentally add unsupported claims or metrics.

Mitigation: Keep facts intact, avoid invented results, and validate bullets against the source candidate material before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jasoncodespace/skills/cv-skill)
- [Input Schema](references/input-schema.md)
- [Rewriting Guide](references/rewriting-guide.md)
- [Harvard HES 2024 Notes](references/harvard-hes-2024-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON input schema, shell commands, and generated DOCX files with optional PDF export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated filenames are sanitized from candidate name and track key; PDF export depends on LibreOffice availability.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
