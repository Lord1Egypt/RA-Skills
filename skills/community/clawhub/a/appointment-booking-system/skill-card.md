## Description: <br>
Generic appointment booking and management system for service businesses, including booking intake, confirmation, automated reminders, no-show follow-up, and daily schedule reports using n8n workflows with a Google Sheets backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Service-business operators and developers use this skill to deploy self-hosted appointment booking workflows for intake, client confirmations, reminders, no-show follow-up, and staff schedule reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public booking and confirmation webhooks can create or change appointments if exposed without controls. <br>
Mitigation: Secure n8n webhooks with authentication or signed expiring per-booking tokens before production use. <br>
Risk: The workflows process customer contact details and appointment records in Google Sheets and email. <br>
Mitigation: Use dedicated Google Sheets and SMTP credentials, restrict sheet and inbox access, and define retention and privacy rules. <br>
Risk: Free-form booking notes may be inserted into email HTML. <br>
Mitigation: Sanitize customer-provided notes before including them in outbound email content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mhmalvi/appointment-booking-system) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, code, guidance] <br>
**Output Format:** [Markdown guidance and n8n workflow JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires n8n, Google Sheets OAuth2 credentials, SMTP credentials, and BUSINESS_NAME, BUSINESS_PHONE, and STAFF_EMAIL environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
