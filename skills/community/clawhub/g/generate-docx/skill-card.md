## Description: <br>
Generate DOCX converts generated or revised content into strictly formatted Word (.docx) documents for 19 Chinese document categories, including government, business, academic, technical, medical, legal, finance, engineering, and general documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FtoIS](https://clawhub.ai/user/FtoIS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-producing agents use this skill to create or reformat Word documents with structured headings, lists, tables, code blocks, captions, signatures, warnings, and document-type-specific Chinese formatting rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and Pandoc tooling to read and write document files. <br>
Mitigation: Install and run it only in a trusted local environment, preferably inside a virtual environment rather than using the documented --break-system-packages pip command. <br>
Risk: Dry-run and show-md modes can display document contents in terminal output. <br>
Mitigation: Use preview modes only with documents whose contents are acceptable to expose in the terminal or logs. <br>
Risk: Reformatted documents may omit or flatten unsupported source-document features such as images, footnotes, and complex merged-cell tables. <br>
Mitigation: Review generated DOCX files before distribution and manually restore unsupported elements when needed. <br>


## Reference(s): <br>
- [ClawHub Generate DOCX Release Page](https://clawhub.ai/FtoIS/generate-docx) <br>
- [Pandoc](https://pandoc.org) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [DOCX files generated from Markdown, with Python API examples and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local python3, python-docx, and Pandoc; can reformat existing .docx files and can print Markdown previews for inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter: 4.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
