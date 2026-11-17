## Description:

Analyzes construction tenders using historical bidding data to assess whether to bid, likely competitors, pricing, qualification requirements, and bid risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Construction contractors and bid teams use this skill to evaluate a specific tender, compare past awards and potential competitors, estimate a price range, and identify qualification or deadline risks before deciding whether to bid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project and company search terms are sent to the provider.

Mitigation: Avoid entering confidential terms without approval to share them with the provider.

Risk: Trial registration uses a MAC-hash-based device check.

Mitigation: Seek informed consent before registration; use an existing API key to skip device registration.

Risk: An API key is stored in a local configuration file.

Mitigation: Limit access to the credential file and do not share the key in reports or conversations.

Risk: Shareable reports may retain signed links that allow access without a normal login prompt.

Mitigation: Restrict report distribution and review embedded links before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/construction-tender-bid-decision)
- [API quick reference](references/api-quick.md)
- [Bid assessment workflow](references/workflow.md)
- [Report template](references/report-template.md)
- [Account registration and credential setup](references/auto-register.md)
- [Provider skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown report, HTML report]

**Output Format:** [Markdown in conversation; optional shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full assessments typically use 12–25 paid API calls; findings should identify evidence and data gaps.]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
