## Description:

Query Flowsery Analytics for real-time visitors, trends, breakdowns, visitor profiles, revenue, conversions, and AI-detected session issues, and create or permanently delete goal and payment records only after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasshyn](https://clawhub.ai/user/tarasshyn)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and developers use this skill to review traffic, visitor behavior, conversions, revenue, and AI-detected site issues across Flowsery-tracked websites. It can also manage goal and payment records when explicitly confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because it exposes issue-status and payment-record changes beyond its declared purpose; the scan is partial.

Mitigation: Review those operations and the partially scanned content before installation, and require explicit confirmation before changing or deleting records.

Risk: Visitor profiles and payment records may contain personal information.

Mitigation: Retrieve individual visitor data only for a specific, authorized request and present only the details needed.

## Reference(s):

- [Flowsery Analytics](https://flowsery.com)
- [Flowsery Analytics API](https://analytics.flowsery.com/analytics/api/v1)
- [Openclaw Flowsery on ClawHub](https://clawhub.ai/tarasshyn/skills/flowsery)

## Skill Output:

**Output Type(s):** [Analysis, Text, Structured API data]

**Output Format:** [Text summaries and structured analytics results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include personal visitor details, revenue, page paths, and session issue information.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
