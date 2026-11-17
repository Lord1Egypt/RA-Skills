## Description:

面向法律/财务/采购场景的合规审计引擎，自动提取风险条款、映射法规基线、生成审计底稿与澄清模板

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, compliance, finance, procurement, and internal-control reviewers use this Chinese-language skill to turn contracts, tender documents, policies, and other business text into compliance risk matrices, audit workpapers, clarification language, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste confidential contract, procurement, or financial details into the agent workflow.

Mitigation: Redact confidential contract details, sensitive amounts, customer names, and other protected information before use.

Risk: Generated legal citations, compliance findings, or law-version assumptions may be incomplete, inaccurate, or outdated.

Mitigation: Have qualified legal, compliance, or internal-control staff verify citations, current law, and material decisions before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/compliance-audit-pro)
- [Skill definition and legal knowledge index](artifact/SKILL.md)
- [README](artifact/README.md)
- [Input schema](artifact/schema.json)
- [Examples](artifact/examples.json)
- [Data Security Law knowledge base](artifact/knowledge/01-data-security-law.md)
- [Cybersecurity Law knowledge base](artifact/knowledge/02-cybersecurity-law.md)
- [Personal Information Protection Law knowledge base](artifact/knowledge/03-personal-info-protection.md)
- [Government Procurement Law knowledge base](artifact/knowledge/04-government-procurement.md)
- [Civil Code Contracts knowledge base](artifact/knowledge/05-civil-code-contracts.md)
- [GDPR knowledge base](artifact/knowledge/09-gdpr.md)
- [Financial compliance knowledge base](artifact/knowledge/16-financial-compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown compliance audit report with tables, workpaper drafts, clarification language, and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static workflow; no code execution, persistence, credential use, or hidden data movement reported by security evidence.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
