## Description:

基于 Qwen2.5-Instruct + RAG 搭建的 AI 法律咨询助手 Skill，覆盖个人创业者 / 中小微企业 / 自媒体的高频法律需求：合同智能审查、合同条款解读、法律法规检索、维权建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzh1998-ui](https://clawhub.ai/user/lzh1998-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product builders, and developers use this skill to design and prompt a China-law oriented AI legal assistant for contract review, clause explanation, legal RAG search, and rights-protection guidance. It is positioned as a decision-support assistant and not as a replacement for licensed legal counsel.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may mistake AI-generated legal guidance for formal legal advice.

Mitigation: Keep disclaimers in user-facing outputs and route high-value, criminal, foreign-related, litigation, real-estate, equity, or other high-risk matters to licensed lawyers.

Risk: Legal questions can include sensitive personal, business, or dispute information.

Mitigation: Add clear privacy and retention notices before real-user use, and instruct users to redact unnecessary sensitive details.

Risk: Claims about lawyer review, data localization, or legal accuracy may be overstated if not independently supported.

Mitigation: Make these claims only when documented, and keep legal-source freshness, citation accuracy, and lawyer-review processes auditable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzh1998-ui/skills/ai-legal-helper)
- [Contract Review](references/contract-review.md)
- [Clause Explanation](references/clause-explanation.md)
- [Legal RAG](references/legal-rag.md)
- [Rights Protection](references/rights-protection.md)
- [Business Model](references/business-model.md)
- [Roadmap](references/roadmap.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with reusable prompt templates, workflows, checklists, and planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include legal disclaimers, cite retrieved legal sources when available, and escalate high-risk cases to licensed lawyers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
