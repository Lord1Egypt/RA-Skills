## Description:

AI合同智能审查助手 reviews Chinese contracts and generates 9-dimension scoring, risk heatmaps, clause revision suggestions, legal references, negotiation guidance, and an interactive HTML review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users reviewing Chinese/PRC-law contracts use this skill to identify legal and business risks, compare suggested clause revisions, and generate an HTML report for human review. It is intended as AI-assisted review and not as final legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can run unsafe contract-derived content.

Mitigation: Avoid attacker-supplied contracts and do not open generated reports until dynamic content is escaped or otherwise sanitized.

Risk: The report template loads external JavaScript despite local/offline positioning.

Mitigation: Remove the CDN dependency or use an integrity-pinned, trusted local copy before relying on offline or sensitive workflows.

Risk: Contract text and generated reports may contain confidential business or legal information.

Mitigation: Avoid highly confidential contracts unless the environment is approved for that data, and delete generated reports when no longer needed.

Risk: The review scope is Chinese/PRC-law contract analysis and may not fit other jurisdictions.

Mitigation: Use the skill only for Chinese/PRC-law contract review and require qualified legal review for material agreements.

## Reference(s):

- [Project homepage](https://github.com/bettermen/contract-review)
- [通用合同审查清单 (General Contract Review Checklist)](references/checklist_general.md)
- [买卖合同审查清单](references/checklist_sales.md)
- [劳动用工合同审查清单](references/checklist_labor.md)
- [租赁合同审查清单](references/checklist_lease.md)
- [服务合同审查清单](references/checklist_service.md)
- [保密协议审查清单](references/checklist_nda.md)
- [投资协议审查清单](references/checklist_investment.md)
- [建设工程合同审查清单](references/checklist_construction.md)
- [技术开发合同审查清单](references/checklist_tech_dev.md)
- [法律条款引用库 (Law Reference Library)](references/law_reference.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown-style review summary with a generated interactive HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is AI-assisted, limited to Chinese/PRC-law contract review, and should be reviewed by a qualified professional before use for important decisions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
