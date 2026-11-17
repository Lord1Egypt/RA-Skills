## Description:

Use this skill when the user asks to research a market, industry, or competitive landscape with a structured credibility-scored protocol for source tiering, cross-validation, graded conclusions, and review iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhitbird](https://clawhub.ai/user/coolhitbird)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, researchers, and product or go-to-market teams use this skill to produce market, industry, or competitive landscape research reports. It structures the work around question definition, tiered source collection, cross-validation, conclusion grading, confidence scoring, and gap review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad research prompts may cause the skill to dominate the interaction scope.

Mitigation: Confirm the research objective, output shape, and search budget before starting, and narrow scope when the user request is ambiguous.

Risk: The source materials are Chinese-first, which may affect language fit for some users.

Mitigation: Review generated reports for the requested language and translate or localize terminology before relying on the output.

Risk: Public market information can be stale, single-sourced, paywalled, or unavailable.

Mitigation: Label uncertain claims as unknown or inference, include timestamps and source tiers, disclose gaps, and recommend human follow-up or first-hand validation where needed.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/coolhitbird/narrative-ops/tree/main/AI%E6%A1%8C%E9%9D%A2%E7%A0%94%E7%A9%B6%E5%91%98)
- [ClawHub skill page](https://clawhub.ai/coolhitbird/skills/ai-2)
- [SOP.md](artifact/SOP.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research reports with evidence links, source credibility scores, graded conclusions, action suggestions, an overall confidence score, and a gap list.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first templates; outputs should include source tiers, timestamps, cross-validation status, and explicit limitations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
