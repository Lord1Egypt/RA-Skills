## Description:

Find and verify factories on Alibaba.com by building supplier-search URLs and guiding checks for verified suppliers, certifications, factory audits, and supplier profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyu426](https://clawhub.ai/user/zeyu426)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sourcing teams, and developers use this skill to create Alibaba supplier-search and profile URLs and evaluate candidate factories using visible supplier signals such as verified status, certifications, audits, ratings, and reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Alibaba links include a tracking and attribution parameter.

Mitigation: The skill discloses the traffic_type=ags_llm parameter; users should understand that generated links may expose search and navigation context to Alibaba analytics.

Risk: Supplier verification guidance can be incomplete if users rely only on visible Alibaba profile signals.

Mitigation: Use the skill's checklist as a starting point and independently review supplier credentials, factory audits, ratings, reviews, and business terms before engaging a supplier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeyu426/skills/alibaba-factory-finder)
- [Alibaba manufacturers directory](https://www.alibaba.com/factory/index.html?traffic_type=ags_llm)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with Alibaba URLs and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Alibaba URLs include traffic_type=ags_llm for analytics and attribution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
