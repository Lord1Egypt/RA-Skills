## Description: <br>
招标文件解析助手可解析 PDF、DOCX 和 TXT 招标文档，提取六类关键信息，并生成带 PDF 原始页码标注的结构化 DOCX 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junqio](https://clawhub.ai/user/junqio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, bidding, and proposal teams use this skill to turn bidding documents into a structured review report that highlights qualification checks, rejection conditions, scoring criteria, technical requirements, binding requirements, and formatting requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bidding documents may contain confidential procurement or commercial information. <br>
Mitigation: Use a trusted workspace, process only documents the user is authorized to share, and review generated reports before distribution. <br>
Risk: Generated TXT, Markdown, and DOCX outputs can overwrite or expose local files if paths are chosen carelessly. <br>
Mitigation: Review output filenames and locations before conversion, and keep generated reports in an appropriate project directory. <br>
Risk: Python helpers require local dependencies such as pdfplumber and python-docx. <br>
Mitigation: Install dependencies only from trusted package sources and review the included scripts before running them in sensitive environments. <br>


## Reference(s): <br>
- [Extraction prompt template](references/extraction_prompt.md) <br>
- [Report format specification](references/report_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables, local TXT extraction files, and DOCX reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include PDF page references when available and may create local Markdown, TXT, and DOCX files in the workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
