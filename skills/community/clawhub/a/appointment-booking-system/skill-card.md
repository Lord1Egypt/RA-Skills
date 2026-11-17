## Description:

Generic appointment booking and management system for service businesses with booking intake, confirmation, automated reminders, no-show followup, and daily schedule reports using n8n workflows with a Google Sheets backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Service-business operators and workflow developers use this skill to deploy appointment booking, confirmation, reminder, no-show followup, and daily schedule-report automation. The workflows support salons, clinics, consultants, studios, repair shops, and similar appointment-based businesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public webhook endpoints can create, confirm, cancel, or otherwise alter appointment records and send email without enough authentication.

Mitigation: Require authentication or signed expiring tokens for status-changing links and webhook calls before production use.

Risk: Public booking intake can be abused for spam, unwanted email, or excessive workflow execution.

Mitigation: Add rate limiting, anti-abuse controls, and monitoring at the n8n ingress layer.

Risk: Customer-supplied fields are written to email and spreadsheet outputs, which can create injection or malformed-content risks.

Mitigation: Apply strict field validation, length limits, HTML escaping, and spreadsheet-formula escaping before storing or sending user input.

Risk: Appointment records include personal contact and scheduling data.

Mitigation: Define a privacy and retention policy, use least-privilege Google Sheets and SMTP credentials, and test first with non-production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhmalvi/skills/appointment-booking-system)

## Skill Output:

**Output Type(s):** [guidance, configuration, code, shell commands]

**Output Format:** [Markdown with JSON workflow references and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses n8n workflow JSON artifacts and requires Google Sheets OAuth2, SMTP, BUSINESS_NAME, BUSINESS_PHONE, and STAFF_EMAIL configuration.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
