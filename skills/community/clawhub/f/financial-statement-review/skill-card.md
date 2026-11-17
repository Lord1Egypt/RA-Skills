## Description:

基于中国《会计法》《企业会计准则》和《税法》体系，对企业财务报表进行合规性审查、风险识别和分析，并支持文件解析、税款比对、收入确认审查、成本操纵识别等策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiliang911](https://clawhub.ai/user/weiliang911)

### License/Terms of Use:

MIT-0

## Use Case:

Auditors, accountants, tax professionals, enterprise finance teams, investors, and analysts use this skill to review Chinese financial statements, identify tax and accounting risks, and generate draft review reports for professional validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive financial files in bulk.

Mitigation: Install and run it only in a controlled environment, and limit inputs to selected financial files or small directories.

Risk: Generated reports may overstate completed checks or appear like final audit or tax opinions.

Mitigation: Treat outputs as draft analysis requiring review by an accountant, tax professional, or other qualified reviewer.

Risk: Large or untrusted PDF and Office inputs may create parser reliability or resource-use concerns.

Mitigation: Use pinned dependencies and avoid untrusted large documents until parser resource limits are added.

## Reference(s):

- [会计法及会计准则要点](references/accounting_law.md)
- [财务报表审查方法论](references/review_methodology.md)
- [中国税法要点摘要](references/tax_law_summary.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports, structured findings, Python examples, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated financial and tax review reports should be treated as draft professional analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata and setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
