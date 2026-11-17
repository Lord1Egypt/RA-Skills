## Description:

cro_skill helps agents assess business risks, analyze likely impacts, and generate response recommendations for market, credit, operational, and related risk categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wen-si](https://clawhub.ai/user/wen-si)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and risk-management teams can use this skill to let an agent classify enterprise risk inputs, summarize financial, reputational, and operational impact, and return mitigation recommendations for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk scores, impact ranges, and recommendations may be too generic or inaccurate for real financial, compliance, or operational decisions.

Mitigation: Require review by qualified risk, compliance, or business-continuity staff before acting on generated assessments.

Risk: The artifact includes publishing commands that require ClawHub CLI credentials.

Mitigation: Run publishing commands only with a pinned, trusted ClawHub CLI in a clean environment with the minimum credentials needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wen-si/skills/croskill)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON object with status, risk type, assessment, impact analysis, recommendations, and timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies; inputs include risk_type, optional company_info, and optional risk_factors.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
