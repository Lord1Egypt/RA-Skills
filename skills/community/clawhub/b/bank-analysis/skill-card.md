## Description: <br>
分析公司银行流水，输出集团总体、收入、支出、应收应付、重大款项及风险分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhilei951](https://clawhub.ai/user/duzhilei951) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance teams and business operators use this skill to analyze local CSV or XLSX bank-statement exports, summarize income, expenses, large transactions, cash-flow trends, receivables/payables, and generate Markdown risk reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank-statement inputs and generated reports may contain confidential financial records. <br>
Mitigation: Run the skill only on trusted local files, keep input files and Markdown reports out of public repositories or broad sync folders, and redact account identifiers or names before sharing reports. <br>
Risk: Spreadsheet files from unknown sources can carry parsing and supply-chain risk. <br>
Mitigation: Prefer trusted CSV inputs when possible, and update the xlsx dependency before opening spreadsheets from untrusted sources. <br>
Risk: Generated financial summaries may be incomplete because bank statements do not fully capture contracts, invoices, or manual receivables/payables context. <br>
Mitigation: Review the report against source statements and supporting finance records before using it for decisions or external reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duzhilei951/bank-analysis) <br>
- [Skill definition](SKILL.md) <br>
- [Usage guide](使用指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Files, Shell commands] <br>
**Output Format:** [Markdown report file with console summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV/XLSX bank-statement files and writes a *_分析报告.md report next to the input file.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
