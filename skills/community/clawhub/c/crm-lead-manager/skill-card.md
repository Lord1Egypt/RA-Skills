## Description:

Manage ad-generated leads and pipeline routing from Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, and landing-page funnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

Marketing, sales operations, and growth teams use this skill to validate ad-generated leads, score lead quality, route prospects to the right owner queues, define follow-up SLAs, and identify pipeline leakage across major advertising channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad advertising or growth questions and produce CRM lead-routing guidance when the user expects general marketing strategy.

Mitigation: Review the output as lead intake, scoring, routing, SLA, and follow-up guidance; use a separate marketing strategy review for broader campaign decisions.

Risk: Incorrect assumptions about lead quality, routing ownership, or response SLAs could misdirect sales follow-up.

Mitigation: Validate required fields, CRM constraints, routing rules, and SLA targets before applying recommendations to production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/crm-lead-manager)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with structured action plans, validation checklists, routing rules, cadence recommendations, and risk alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep channel-specific advertising guidance distinct, separate observed facts from assumptions, and include rollback or stop-loss conditions when spend risk exists.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
