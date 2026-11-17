## Description:

建设工程商事调解知识图谱专家技能，用于工程纠纷分析、商事调解策略、调解流程设计、利益方识别、争议焦点梳理、BATNA/WATNA评估和调解协议起草。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

External mediators, lawyers, cost engineers, project managers, and agents use this skill to diagnose construction disputes, design mediation workflows, assess negotiation positions, retrieve legal or case references, and draft mediation documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send case details, evidence, or settlement strategy to third-party AI services.

Mitigation: Use only with consent, review provider terms, and anonymize sensitive data before external calls.

Risk: Case and evidence records may be stored locally in plaintext.

Mitigation: Run with restricted filesystem access and store records only in protected locations with encryption or equivalent controls.

Risk: The security review notes a provider-routing issue affecting the Zhipu provider.

Mitigation: Avoid the Zhipu provider until the implementation is corrected and retested.

Risk: Generated mediation analysis or agreement drafts may be incomplete or unsuitable for a specific dispute.

Mitigation: Have qualified legal professionals review outputs before relying on them in a mediation or settlement process.

## Reference(s):

- [Construction Mediation Kg ClawHub Page](https://clawhub.ai/ruiyongwang/skills/construction-mediation-kg)
- [Dispute Types](references/dispute-types.md)
- [BATNA / WATNA Framework](references/batna-framework.md)
- [Mediation Strategies](references/mediation-strategies.md)
- [Legal Basis](references/legal-basis.md)
- [Agreement Template](references/agreement-template.md)
- [Farui Quickstart](scripts/farui_quickstart.md)
- [V2 Quickstart](scripts/v2_quickstart.md)
- [Alibaba Cloud Bailian Platform](https://bailian.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, structured reports, Python snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include legal and mediation references, document drafts, case-management records, evidence summaries, and third-party AI service guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
