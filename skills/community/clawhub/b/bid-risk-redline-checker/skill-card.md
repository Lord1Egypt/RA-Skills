## Description:

Analyzes tender notices and historical bidding data for restrictive terms, competition signals, pricing context, and bid-or-no-bid decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and bidders use this skill to assess a specific tender's disqualification risks, restrictive conditions, likely competitors, historical pricing, and whether to bid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid, company, and project queries are sent to Zhiliaobiaoxun.

Mitigation: Confirm the data is appropriate to share with the provider before running an analysis.

Risk: The skill may create an API account and store its key locally.

Mitigation: Require consent before registration and protect the locally stored key.

Risk: Exported reports may contain signed links that grant access to vendor resources.

Mitigation: Treat HTML reports as sensitive and restrict sharing to intended recipients.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/bid-risk-redline-checker)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Analysis workflow](references/workflow.md)
- [Report template](references/report-template.md)
- [Registration and credential handling](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown decision report and optional shareable HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a recommendation, supporting evidence, confidence, pricing guidance, and data gaps.]

## Skill Version(s):

1.0.9 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
