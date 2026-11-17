## Description:

A workflow skill for creating and managing email marketing campaigns, including Resend email delivery, click and conversion tracking, campaign reporting, reminder sends, and trial activation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and growth operators use this skill to implement and operate campaign records, email templates, tracking queries, reminder sends, and trial activation workflows for email marketing campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes patterns for production email sending and subscription trial activation, which can change customer-facing state if used without authorization.

Mitigation: Use the skill only with authorized operators, require explicit approval gates for sends and subscription changes, and default campaign scripts to dry-run behavior.

Risk: Recipient email addresses may be exposed through personalized campaign links or mishandled recipient lists.

Mitigation: Validate recipient lists before sending, prefer opaque campaign tokens instead of raw email query parameters, and avoid logging unnecessary recipient data.

Risk: Bulk campaign sends can exceed provider limits or send to unintended recipients.

Mitigation: Enforce the documented Resend rate limit, add production-environment safeguards, and test templates against a controlled recipient list before launch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/email-campaign-management)
- [Resend email API endpoint referenced by the skill](https://api.resend.com/emails)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, Python, HTML/CSS, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow checklists, query patterns, template requirements, and operational cautions for email campaigns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
