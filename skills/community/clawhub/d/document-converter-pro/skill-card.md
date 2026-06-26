## Description: <br>
Document format converter for converting between Word, PDF, Markdown, and HTML formats, including docx-to-pdf, md-to-pdf, md-to-docx, and html-to-pdf workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document authors use this skill to generate local conversion commands and code for transforming documents between DOCX, PDF, Markdown, HTML, and plain text formats while preserving common structure such as headings, lists, tables, and fonts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML-to-PDF conversion can include local files referenced by input HTML in the generated PDF. <br>
Mitigation: Convert trusted HTML only, or run HTML-to-PDF conversion in a sandbox or controlled directory. <br>
Risk: Local conversion requires installing Python packages and, for HTML-to-PDF, an optional system binary. <br>
Mitigation: Install dependencies only in an environment where running local conversion commands is acceptable. <br>


## Reference(s): <br>
- [Conversion Matrix](references/conversion-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local conversion guidance; HTML-to-PDF requires optional wkhtmltopdf.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
