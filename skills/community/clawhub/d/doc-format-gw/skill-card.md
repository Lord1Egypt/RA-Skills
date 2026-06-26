## Description: <br>
公文排版工具 - 根据公文格式规范自动排版Word文档。适用于发送Word文件前进行格式调整。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batduke](https://clawhub.ai/user/batduke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, document preparers, and agents use this skill to reformat Word documents before sending them as official Chinese government-style documents. It applies heading, body text, table, margin, line-spacing, and page-number formatting rules from the bundled reference material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formatting a Word document can change important layout details or overwrite a needed output path. <br>
Mitigation: Use a separate output filename and keep backups of sensitive or important documents. <br>
Risk: The formatter depends on local Python packages and document fonts, which can affect execution or visual results. <br>
Mitigation: Install python-docx from a trusted Python environment and confirm required fonts are available before relying on the formatted document. <br>


## Reference(s): <br>
- [Format Rules](references/format-rules.md) <br>
- [ClawHub release page](https://clawhub.ai/batduke/doc-format-gw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown usage guidance with bash and Python examples; formatted .docx files when the script is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and python-docx; reads a user-selected .docx file and writes a formatted output .docx file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
