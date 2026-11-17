## Description:

招投标助手（Bid Assistant）。协助完成从机会识别、评估、标书解析、评分模型建立，到方案结构设计、正文撰写辅助、表达净化与提交前一致性审查的完整招投标流程。本工具由 @afeicn 提供支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Market, business, proposal, bid, and management teams use this skill to turn tender notices and bid materials into opportunity summaries, feasibility checks, scoring models, response outlines, draft bid sections, and pre-submission review reports. It is especially oriented toward government procurement technical-service bids and keeps final bid decisions, pricing, commitments, seals, and submission under human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender workflows may handle customer information, pricing material, company qualifications, historical bids, and business strategy.

Mitigation: Before installation, confirm that only authorized users can submit materials and configure retention, audit logs, sensitive-information masking, and Feishu permissions.

Risk: Generated recommendations could affect high-impact bid/no-bid decisions, pricing, commitments, seals, or final submission.

Mitigation: Keep final decisions, pricing, business commitments, qualification truthfulness, seals, and submission under explicit human approval.

Risk: Draft bid content may contain sample-project residue, unsupported qualifications, internal scoring language, or AI-style phrasing.

Mitigation: Use the skill's pre-submission review, expression cleanup, no-negative-deviation index, and human confirmation steps before any formal bid use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/bid-assistant)
- [README.md](README.md)
- [workflows.md](workflows.md)
- [runbook.md](runbook.md)
- [knowledge/README.md](knowledge/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown reports, tables, checklists, outlines, and draft sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include opportunity briefs, tender analysis reports, scoring models, task lists, service-scheme structures, draft bid sections, cleanup reports, chart placeholder catalogs, consistency checks, and retrospective summaries.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact README.md and employee.yaml list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
