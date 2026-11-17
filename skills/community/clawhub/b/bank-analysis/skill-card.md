## Description:

分析公司银行流水，输出集团总体、收入、支出、应收应付、重大款项及风险分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users can analyze company bank-statement CSV or XLSX exports to summarize cash flow, income, expenses, receivables and payables, large transactions, and financial risk signals. The skill is intended for local report generation from trusted financial files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive bank-statement data and generated reports may contain transaction details.

Mitigation: Run it only on trusted local inputs, restrict access to the working directory, and delete or protect generated reports after use.

Risk: The release uses a flagged XLSX parser version.

Mitigation: Update or replace the xlsx dependency before production use and avoid opening untrusted spreadsheet files.

Risk: Spreadsheet text is written into Markdown reports without sanitation.

Mitigation: Use trusted input files, sanitize untrusted spreadsheet text before sharing reports, and avoid Markdown viewers that load remote content for untrusted reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhilei951/skills/bank-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/duzhilei951)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with console text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a cleartext Markdown report next to the input CSV or XLSX file.]

## Skill Version(s):

2.0.0 (source: server evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
