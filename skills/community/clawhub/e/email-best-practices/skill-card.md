## Description:

Use when building email features, emails going to spam, high bounce rates, setting up SPF/DKIM/DMARC authentication, implementing email capture, ensuring compliance (CAN-SPAM, GDPR, CASL), handling webhooks, retry logic, or deciding transactional vs marketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christina-de-martinez](https://clawhub.ai/user/christina-de-martinez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to design, implement, and troubleshoot deliverable, compliant email systems for transactional and marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook and privacy examples may be unsafe if copied directly into production.

Mitigation: Treat examples as reference material; verify webhook signatures over the raw request body, validate verified event schemas, and review implementation details before deployment.

Risk: Email workflows can expose sensitive recipient, event, location, or engagement data.

Mitigation: Limit raw payload logging, define retention and access controls, and review consent and privacy requirements before using re-engagement campaigns or IP/location details.

## Reference(s):

- [Email Best Practices Skill Documentation](https://resend.com/docs/email-best-practices-skill)
- [Email Best Practices Repository](https://github.com/resend/email-best-practices)
- [Email Compliance](references/compliance.md)
- [Email Deliverability](references/deliverability.md)
- [Email Capture Best Practices](references/email-capture.md)
- [Email Types: Transactional vs Marketing](references/email-types.md)
- [List Management](references/list-management.md)
- [Marketing Email Best Practices](references/marketing-emails.md)
- [Sending Reliability](references/sending-reliability.md)
- [Transactional Email Catalog](references/transactional-email-catalog.md)
- [Transactional Email Best Practices](references/transactional-emails.md)
- [Webhooks and Events](references/webhooks-events.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, command examples, tables, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes email compliance, deliverability, webhook, retry, suppression, and list-management recommendations.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
