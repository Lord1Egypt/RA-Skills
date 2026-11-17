## Description:

Frontend Cv creates professional HTML and PDF-ready resumes from PDF, Word, Markdown, text, YAML, or JSON inputs, with structured resume data and selectable themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vintlin](https://clawhub.ai/user/vintlin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert, redesign, or build resumes into print-ready HTML and browser-exported PDFs with theme previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated resume data, previews, and HTML files may contain personal information.

Mitigation: Review where generated files are stored before opening or sharing them, and remove temporary previews or extracted text when they are no longer needed.

Risk: Untrusted resume or YAML inputs may be processed by local extraction and rendering scripts.

Mitigation: Use a virtual environment and review inputs before running the bundled scripts, especially for documents from untrusted sources.

Risk: Some themes reference remote font URLs that may be loaded by the browser.

Mitigation: Work offline or remove remote font links when handling sensitive resumes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vintlin/skills/frontend-cv)
- [HTML Shell](references/html-template.md)
- [RenderCV Theme Presets](references/theme-presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [YAML resume data, self-contained HTML resume files, Markdown guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may contain personal resume data and remote font links depending on the selected theme.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
