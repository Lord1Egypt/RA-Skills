## Description:

Interact with FundraiseUp REST API to manage donations, recurring plans, supporters, campaigns, and donor portal access. Process online and offline donations, retrieve fundraising analytics, and integrate with nonprofit CRM systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aamish99](https://clawhub.ai/user/aamish99)

### License/Terms of Use:

MIT

## Use Case:

Developers and nonprofit operations teams use this skill to work with FundraiseUp API resources for donation processing, donor and recurring-plan management, campaign reporting, donor portal access, and CRM integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle live donations and donor data.

Mitigation: Review before production use, start with test-mode keys, use least-privilege API permissions, and require explicit user approval before creating or updating donations or generating donor portal links.

Risk: Authorization headers, donor portal links, payment-method identifiers, or donor request and response bodies could expose sensitive data if logged.

Mitigation: Do not log authorization headers, donor portal links, payment-method identifiers, or full donor request and response bodies.

Risk: Donor portal links provide short-lived access to sensitive supporter and payment information.

Mitigation: Validate supporter ownership, use automatic redirects, and do not share portal links over email, SMS, or public channels.

## Reference(s):

- [FundraiseUp REST API Documentation](https://fundraiseup.com/docs/rest-api/)
- [FundraiseUp API Resources](https://fundraiseup.com/docs/rest-api-resources/)
- [FundraiseUp Seamless Donor Portal](https://fundraiseup.com/docs/seamless-donor-portal/)
- [ClawHub Skill Page](https://clawhub.ai/aamish99/skills/fundraiseup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, JavaScript, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FUNDRAISEUP_API_KEY for authenticated FundraiseUp API use.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
