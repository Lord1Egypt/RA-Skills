## Description:

Screens Chinese tender and procurement documents for bid-rejection clauses, hard qualification requirements, bid bond requirements, and hidden risks, then produces a structured checklist for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, bid, and compliance reviewers use this skill to inspect Chinese tender documents before submission, identify rejection risks, and assign checklist items for manual verification. It is not intended for legal determinations, bid drafting, scoring, complaints, or pricing strategy.

### Deployment Geography for Use:

Global; intended for Chinese tender and procurement review contexts.

## Known Risks and Mitigations:

Risk: Users may treat the checklist as legal advice or a final bid/no-bid decision.

Mitigation: Use the output as a human-review checklist and have qualified procurement or legal reviewers verify the source terms before acting.

Risk: Incomplete files, poor OCR, or missing tender sections may cause missed or misread rejection risks.

Mitigation: Provide complete tender files and manually verify cited clauses, page numbers, amounts, dates, and confidence labels.

Risk: Users may ask for pricing strategy, bid drafting, scoring analysis, complaints, or fabricated qualification material.

Mitigation: Keep use limited to rejection-risk extraction and checklist generation; route out-of-scope requests to appropriate human or specialist review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-rejection-risk-radar)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact manifest](artifact/manifest.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured risk checklist with risk levels, confidence labels, source locations, verification actions, responsible-owner placeholders, and final bid-submission checks.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
