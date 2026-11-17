## Description:

Reviews and drafts financial product marketing content against financial marketing rules, industry-specific controls, and risk disclosure patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, marketing, and product teams use this skill to review financial product articles, campaign plans, and industry-specific copy, and to draft marketing plans with risk notes and revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may incorrectly label risky financial marketing content as compliant.

Mitigation: Treat all outputs as drafting aids and require review by qualified legal, compliance, and product owners before publication.

Risk: The skill requests broad agent powers, including shell and write-oriented tools.

Mitigation: Run with read-only project access and without general shell or write privileges unless a reviewer explicitly approves a bounded operation.

Risk: Financial regulations and enforcement expectations can change or vary by jurisdiction.

Mitigation: Confirm cited rules, effective dates, and jurisdictional applicability against current authoritative sources before relying on the output.

## Reference(s):

- [金融监管法规汇编](references/regulations.md)
- [审查规则库](references/rules.md)
- [金融违规处罚案例库](references/cases.md)
- [金融风险提示模板库](templates/disclaimers.md)
- [合规审查报告模板](templates/review-report.md)
- [合规检查脚本](scripts/compliance-checker.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style review reports, generated marketing-plan text, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include compliance status, risk level, cited rule labels, warnings, and suggested revisions; they require human legal and compliance review before publication.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
