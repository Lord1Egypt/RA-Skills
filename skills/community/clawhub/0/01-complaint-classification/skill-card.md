## Description:

Classifies user complaints against GB/T 42499-2023 and Alibaba platform rules, assigns priority, estimates the initially responsible party, and recommends routing for Cainiao Logistics, Cainiao Station, and Taobao Flash Purchase workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal complaint operations staff use this skill to triage complaint text, ticket details, or batches of complaints into structured categories, priority levels, preliminary responsibility assessments, and handling paths. Its output is advisory and should be reviewed by the responsible team before liability, compensation, penalty, or retention decisions are finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complaint records may contain personal, order, or account data.

Mitigation: Redact sensitive data unless approved organizational handling and retention controls are in place.

Risk: Classification, routing, priority, liability, compensation, or penalty recommendations may be incorrect or incomplete.

Mitigation: Treat outputs as advisory and require review by the responsible internal team before final action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/01-complaint-classification)
- [GB/T 42499-2023 complaint classification standard](artifact/SKILL.md)
- [Complaint classification rules manual](artifact/RULES.md)
- [Complaint classification examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured complaint classification fields and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-complaint mode returns classification, priority, responsibility, routing, and remarks; batch mode returns summary distributions, high-risk items, anomalies, and dispatch totals.]

## Skill Version(s):

1.0.0 (source: server release metadata; source skill frontmatter states 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
