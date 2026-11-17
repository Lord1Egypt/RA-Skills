## Description:

恋爱避雷针 analyzes user-provided dating chat excerpts for recurring risky relationship patterns and returns a cautious report with evidence snippets, a warning level, and practical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chujindan-dotcom](https://clawhub.ai/user/chujindan-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review their own dating or flirtation chat excerpts for recurring warning signs such as manipulation, ambiguity, avoidance, or control. It helps separate stronger patterns from insufficient evidence and returns a short relationship risk report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-label another person when the chat excerpt is incomplete or lacks a repeated pattern.

Mitigation: Use the artifact's guardrails: rely on recurring patterns, mark insufficient evidence as observation, and include the stated disclaimer that the report is not factual proof.

Risk: User-submitted relationship chat logs can include sensitive private information.

Mitigation: Share only excerpts the user is comfortable processing, and minimize or anonymize private details where possible.

Risk: PUA, control, or safety-related scenarios may involve real-world harm beyond chat analysis.

Mitigation: Reduce humor in serious scenarios and recommend support from trusted people, professionals, or legal channels when safety concerns appear.

## Reference(s):

- [渣谱系库（11 款）](references/archetypes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown report card with quoted evidence snippets, labels, warning level, and brief advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided chat excerpts and may ask 1-2 clarifying questions when evidence is insufficient.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
