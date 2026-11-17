## Description:

Use when user needs Amazon push score calculation and optimization strategy for Amazon listing performance, A9 optimization planning, traffic tier classification, and CTR/CVR improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon marketplace operators and ecommerce teams use this skill to score listings from manually supplied CTR, CVR, seven-day growth, and account health metrics, then receive traffic pool classification and prioritized optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The score and benchmarks may be mistaken for verified Amazon algorithm data.

Mitigation: Treat outputs as operational guidance based on manually supplied metrics and validate decisions against seller platform data and business judgment.

Risk: The skill may activate during broad Amazon CTR, CVR, ranking, or A9 discussions.

Mitigation: Confirm that the user wants Amazon push score analysis before applying the scoring workflow.

## Reference(s):

- [Amazon industry benchmark reference](artifact/references/benchmarks.md)
- [CloudTrip homepage](https://cloudtrip.ai)
- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/amazon-push-score)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with score calculation, tier classification, benchmark comparison, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires four manually supplied listing metrics; does not access Amazon accounts, install code, or run external tools.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
