## Description:

上市公司审计追踪与风险检测技能包，自动化分析往来账龄、标记异常交易、检测重复付款、监控大额异常预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aolikeji](https://clawhub.ai/user/aolikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, audit, compliance, and risk teams use this skill to analyze receivable and payable aging, detect anomalous transactions, flag duplicate payments, review bank reconciliation issues, assess expense and tax risks, and draft audit findings for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive finance, audit, tax, and transaction data.

Mitigation: Use only data the user is authorized to process, minimize shared datasets, and follow the organization's confidentiality controls.

Risk: Broad finance and audit triggers may cause the skill to activate in contexts where automated risk labels could be over-read.

Mitigation: Review outputs carefully and treat freezes, collections, tax actions, and risk ratings as recommendations requiring professional human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aolikeji/skills/finance-audit-tracker)
- [Project homepage](https://github.com/AOLIKEJI/finance-audit-tracker)
- [Publisher profile](https://clawhub.ai/user/aolikeji)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports, tables, JSON examples, and audit-rule pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be treated as audit assistance and reviewed by qualified finance, audit, tax, or compliance personnel before action.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
