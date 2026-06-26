## Description: <br>
Use when building email features, emails going to spam, high bounce rates, setting up SPF/DKIM/DMARC authentication, implementing email capture, ensuring compliance (CAN-SPAM, GDPR, CASL), handling webhooks, retry logic, or deciding transactional vs marketing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christina-de-martinez](https://clawhub.ai/user/christina-de-martinez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, troubleshoot, and operate email features, including deliverability, authentication, transactional and marketing email choices, compliance checks, webhook handling, retry behavior, and list hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email implementation examples may involve sensitive data such as email addresses, webhook payloads, IP addresses, locations, API keys, and webhook secrets. <br>
Mitigation: Treat those values as sensitive, minimize what is placed in emails and logs, protect secrets, and set retention limits before production use. <br>
Risk: Compliance guidance may not fully cover the user's jurisdiction or business-specific obligations. <br>
Mitigation: Confirm legal requirements for the relevant jurisdictions before relying on unsubscribe, consent, retention, or marketing-email practices. <br>
Risk: Deliverability and sending recommendations can affect production email reliability and sender reputation if applied incorrectly. <br>
Mitigation: Review DNS authentication, retry behavior, suppression handling, and list hygiene changes in a controlled environment before broad rollout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/christina-de-martinez/email-best-practices) <br>
- [Resend Email Best Practices Documentation](https://resend.com/docs/email-best-practices-skill) <br>
- [Resend Email Best Practices Repository](https://github.com/resend/email-best-practices) <br>
- [Resend Agent Skills](https://resend.com/agent-skills) <br>
- [Compliance](references/compliance.md) <br>
- [Deliverability](references/deliverability.md) <br>
- [Email Capture Best Practices](references/email-capture.md) <br>
- [Email Types: Transactional vs Marketing](references/email-types.md) <br>
- [List Management](references/list-management.md) <br>
- [Marketing Emails](references/marketing-emails.md) <br>
- [Sending Reliability](references/sending-reliability.md) <br>
- [Transactional Email Catalog](references/transactional-email-catalog.md) <br>
- [Transactional Emails](references/transactional-emails.md) <br>
- [Webhooks and Events](references/webhooks-events.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, tables, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; users adapt examples to their email provider, jurisdiction, and production controls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
