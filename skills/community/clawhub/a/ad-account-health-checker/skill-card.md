## Description:

Assess ad account readiness and risk status across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

External marketing, growth, and advertising operators use this skill to assess ad account structure, permissions, policy risk, billing state, and launch readiness before running or scaling campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget, bidding, billing, policy, or launch recommendations can affect real advertising accounts and spend.

Mitigation: Verify source data, platform permissions, compliance constraints, and a rollback plan before applying recommendations.

Risk: Low-quality or incomplete account data can lead to overconfident campaign guidance.

Mitigation: Treat missing inputs as assumptions, request critical follow-up fields, and prefer reversible low-risk actions when uncertainty is high.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/ad-account-health-checker)
- [Publisher profile](https://clawhub.ai/user/danyangliu-sandwichlab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured sections for intent summary, findings, action plan, risks and guardrails, and handoff payload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output should separate facts from assumptions and avoid applying budget, bidding, billing, policy, or launch changes without verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
