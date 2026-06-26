## Description: <br>
AI-powered booking manager that connects to existing booking systems so business owners can monitor appointments, respond through phone channels, send customer emails, and generate calendar invites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cskar10](https://clawhub.ai/user/cskar10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners and operations staff use this skill to manage appointment enquiries, confirmations, reschedules, cancellations, reminders, and schedule summaries through supported phone or chat channels. Developers and administrators use it to connect booking data sources, SMTP email, and calendar-invite workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access booking data and customer contact details while operating real appointments. <br>
Mitigation: Use dedicated least-privilege booking-system credentials, keep secrets out of chat and workspace notes, and review data-use expectations with staff and customers. <br>
Risk: Email, SMS, WhatsApp, Telegram, or call-routing workflows may contact customers with incorrect or unintended appointment information. <br>
Mitigation: Review TOOLS.md and HEARTBEAT.md changes before relying on automation, validate business policies during onboarding, and test notification templates before production use. <br>


## Reference(s): <br>
- [Booking Manager on ClawHub](https://clawhub.ai/cskar10/booking-manager) <br>
- [Data Source Connection Patterns](references/data-sources.md) <br>
- [Email Templates](references/email-templates.md) <br>
- [ICS Calendar Invite Format](references/ics-format.md) <br>
- [Booking Manager Customer Onboarding Form](references/onboarding-form.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown with configuration snippets, SQL examples, email templates, and calendar invite content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces appointment-management instructions and customer-facing message content; execution depends on configured booking data source and SMTP credentials.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
