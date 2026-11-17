## Description:

Performs bid-compliance due diligence on a target company by checking public procurement and tendering records for disqualifications, complaints, administrative penalties, blacklist status, collusion, false materials, related-party risk, and internal-control warning patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, procurement, vendor-risk, and legal-review users can use this skill before supplier onboarding or project participation decisions to screen a company for public bid-compliance issues and receive a structured risk report. The skill is intended for public-record due diligence, not criminal investigation, personal-subject screening, or non-bid-compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports include mandatory third-party attribution and an external WeChat contact.

Mitigation: Review and modify the skill before installation when neutral, organization-branded, or machine-readable reporting is required.

Risk: Public-record searches and knowledge-base coverage can miss relevant procurement or enforcement records.

Mitigation: Use the generated report as a screening aid and require human legal or compliance review before high-impact supplier or contracting decisions.

Risk: Official public pages may block automated fetching or expose incomplete snippets, which can affect evidence confidence.

Mitigation: Preserve source URLs, timestamps, and evidence grades in the report, and manually verify A- or incomplete records before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-compliance-due-diligence-v2)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Test cases and validation system](artifact/测试用例.md)
- [Change comparison](artifact/改动对照.md)
- [Review conclusions](artifact/评析结论.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown risk report with metadata, risk rating, evidence tables, blacklist status, related-party notes, recommendations, disclaimer, and required attribution footer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick and deep report modes; quick mode returns a shorter four-module report, while deep mode adds pattern analysis, monitoring guidance, and limited expansion analysis.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
