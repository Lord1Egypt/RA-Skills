## Description: <br>
读取和编辑 Word、PDF、Excel 文档。使用 python-docx、pdfplumber、openpyxl <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract text from Word, PDF, and Excel files and to follow documented document-processing command examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose contents of local Word, PDF, or Excel files to the agent when those files are provided. <br>
Mitigation: Use it only with documents intended for agent access and avoid sensitive files unless disclosure is intended. <br>
Risk: The skill depends on external Python packages for document parsing. <br>
Mitigation: Install python-docx, pdfplumber, openpyxl, and pandas from trusted package sources in a controlled environment. <br>
Risk: The release advertises write/edit support, but the included script only implements reading behavior. <br>
Mitigation: Treat write/edit capability as unsupported in this version and verify outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xaiohuangningde/doc-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local document files supplied by the user; write/edit behavior is advertised but unsupported by the included script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
