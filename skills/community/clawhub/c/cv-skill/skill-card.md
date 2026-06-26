## Description: <br>
Create professional Harvard-style resumes, CVs, and matching cover letters from user-provided candidate descriptions, structured data, or existing resumes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasoncodespace](https://clawhub.ai/user/jasoncodespace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn candidate notes, structured JSON, or existing resumes into role-targeted Harvard-style resumes and matching cover letters. It supports multiple tracks, concise factual rewriting, DOCX generation, and optional PDF export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes resume and cover-letter data supplied by the user, which may include personal information. <br>
Mitigation: Review candidate JSON before use and keep generated outputs in the intended local folder. <br>
Risk: Optional PDF export relies on local LibreOffice document conversion. <br>
Mitigation: Use PDF export only in an environment where LibreOffice conversion is acceptable, or generate DOCX output only. <br>
Risk: Installing dependencies changes the local Python environment. <br>
Mitigation: Approve pip installation only when needed and review requirements.txt before installing. <br>


## Reference(s): <br>
- [CV Skill on ClawHub](https://clawhub.ai/jasoncodespace/cv-skill) <br>
- [Input Schema](references/input-schema.md) <br>
- [Rewriting Guide](references/rewriting-guide.md) <br>
- [Harvard HES 2024 Notes](references/harvard-hes-2024-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [DOCX files, optional PDF files, Markdown guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one resume per selected track from structured candidate JSON; optional cover letter content is used when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
