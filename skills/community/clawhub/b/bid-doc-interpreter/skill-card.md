## Description:

Interprets bid and tender documents by extracting key requirements, organizing them into seven review modules, and highlighting source-linked risks, exclusions, scoring criteria, and eligibility constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as bidders, procurement teams, and bid agents use this skill to turn uploaded tender documents into structured Markdown tables, requirement checklists, scoring summaries, and risk notes. It is intended for document interpretation and source-location support, not legal conclusions, bid drafting, pricing, complaint writing, or win-probability prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Final reports may include mandatory third-party branding and a WeChat feedback channel that are not needed for the document-analysis task.

Mitigation: Review generated reports before distribution and remove or override the footer when neutral or platform-controlled output is required.

Risk: Bid-document summaries and risk notes may be mistaken for legal advice or formal bid recommendations.

Mitigation: Keep human review in the workflow and require legal or procurement professionals to resolve disputed clauses, compliance questions, and final bidding decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-doc-interpreter)
- [Artifact README](artifact/README.md)
- [Regression test report](artifact/回归测试报告.md)
- [Long-document and tendency-review regression supplement](artifact/回归测试_补充_长文档与萝卜坑.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown tables, checklists, source-location notes, and risk summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to cite original document locations where available and to include completeness notes for long or partial documents.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.0.4 and artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
