## Description: <br>
公文格式排版工具，将 doc/docx/wps/txt/md 文档按照公文排版习惯自动格式化，输出标准 docx。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwyalpha](https://clawhub.ai/user/cwyalpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, staff, and document operations users use this skill to format Chinese official documents, normalize headings, page layout, fonts, line spacing, attachments, tables, and batch document outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recursively read and process folders passed by the user, which may include more private documents than intended. <br>
Mitigation: Pass only the specific files or narrow folders intended for formatting, and avoid broad private directories unless recursive processing is desired. <br>
Risk: Generated DOCX files may not preserve every layout detail, especially for legacy Office or WPS inputs that require local Office or LibreOffice conversion. <br>
Mitigation: Review generated documents before relying on them, with extra attention to titles, headings, attachments, page numbers, tables, and automatic numbering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cwyalpha/doc-format) <br>
- [CLI Reference](artifact/references/cli-reference.md) <br>
- [Config Reference](artifact/references/config-reference.md) <br>
- [Formatting Rules](artifact/references/formatting-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated DOCX files and optional JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces formatted DOCX copies from explicitly provided input files or folders; successful output paths are printed to stdout.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
