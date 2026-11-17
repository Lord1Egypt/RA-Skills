## Description:

AI marketing department for contractors and home service businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueprintstudioco](https://clawhub.ai/user/blueprintstudioco)

### License/Terms of Use:

MIT-0

## Use Case:

Contractors and home service businesses use this skill to generate and review local marketing assets, including SEO plans, Google Business Profile posts, social media content, ad campaigns, proposals, review responses, competitor audits, job costing summaries, email sequences, and lead follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent business profile storage, which can include sensitive business details.

Mitigation: Confirm where memory is stored and how to edit or delete it before saving business profile data.

Risk: Recurring cron-style automation can publish, report, or check reviews on a schedule without enough user control.

Mitigation: Confirm each schedule and command before enabling recurring automation.

Risk: The strategy-library lookup connects to an external Supabase service.

Mitigation: Avoid sending confidential business context to the external service without user approval.

## Reference(s):

- [Contractor Marketing ClawHub release](https://clawhub.ai/blueprintstudioco/skills/contractor-marketing)
- [Ad Creative Angles](references/ad-creative-angles.md)
- [Business Profile Onboarding Questions](references/onboarding-questions.md)
- [Proposal Template](references/proposal-template.md)
- [Review Response Rules](references/review-response-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, HTML snippets, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce recurring task suggestions, proposal HTML, marketing calendars, ad copy, review responses, reports, and follow-up sequences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
