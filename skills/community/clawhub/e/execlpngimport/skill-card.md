## Description:

Excel/截图字段智能导入工具。将 Excel 数据源或截图（PDU截图）中的字段，按照固定模板格式自动导入，生成标准化的导入模板。支持中英文字段名映射、字段类型智能识别、截图 OCR 识别。适用于资产负债表、现金流量表、利润表、银行账号等财务报表批量导入场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitxiajp](https://clawhub.ai/user/gitxiajp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to turn Excel, CSV, or screenshot inputs into standardized Excel import templates for financial reports, bank account lists, and custom forms. It can extract field names, map Chinese labels to English identifiers, infer field types, and write the resulting template workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workbook cells may preserve unsafe formula-like values from source data.

Mitigation: Sanitize field values before saving and review generated workbooks before opening or sharing them.

Risk: Output paths may overwrite existing files or write templates to unintended locations.

Mitigation: Use explicit output paths in an isolated workspace and confirm filenames before execution.

Risk: OCR screenshots and financial spreadsheets may contain confidential or regulated data.

Mitigation: Process only approved data, avoid regulated screenshots unless permitted, and delete temporary files after review.

Risk: Dependencies are installed without pinned versions.

Mitigation: Pin and review dependency versions before installing in shared or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitxiajp/skills/execlpngimport)
- [ClawHub publisher profile](https://clawhub.ai/user/gitxiajp)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python snippets and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided Excel, CSV, or image inputs and the selected template path.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
