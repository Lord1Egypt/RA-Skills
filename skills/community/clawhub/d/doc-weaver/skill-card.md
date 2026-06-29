## Description: <br>
Transform Markdown or outlines into polished Word/PDF documents with professional templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document authors use this skill to convert Markdown or structured outlines into polished Word, PDF, or preview documents using built-in templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Markdown is processed by local document-conversion tooling. <br>
Mitigation: Review input files and output paths before running commands, and handle untrusted Markdown as local converter input. <br>
Risk: PDF generation requires optional local pandoc and weasyprint dependencies. <br>
Mitigation: Run the documented doctor check before PDF conversion; use Word output when PDF dependencies are unavailable. <br>


## Reference(s): <br>
- [Doc Weaver README](README.md) <br>
- [Template Reference](references/templates.md) <br>
- [Doc Weaver ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/doc-weaver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts may be .docx, .pdf, or Markdown preview text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local document conversion; PDF output depends on pandoc and weasyprint, while Word output depends on python-docx.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
