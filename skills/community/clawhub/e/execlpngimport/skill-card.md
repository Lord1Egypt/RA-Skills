## Description: <br>
Excel/截图字段智能导入工具，可从 Excel 数据源或截图中提取字段，映射中英文字段名，识别字段类型，并生成标准化导入模板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitxiajp](https://clawhub.ai/user/gitxiajp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance operations teams use this skill to convert Excel files or report screenshots into standardized import templates for balance sheets, cash flow statements, income statements, bank account lists, and custom forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process financial spreadsheets or screenshots supplied by the user. <br>
Mitigation: Use it only with files intended for local processing and review generated templates before importing them into business systems. <br>
Risk: OCR can miss or misread fields in screenshots, and the OCR dependency may download models on first use. <br>
Mitigation: Inspect OCR results and the first rows of the generated template before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitxiajp/execlpngimport) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Excel template files and Markdown guidance with inline Python and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates should be reviewed for OCR accuracy, field mappings, field types, and required-column placement before business use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
