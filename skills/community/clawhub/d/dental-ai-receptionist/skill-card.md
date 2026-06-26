## Description: <br>
Complete AI voice receptionist system for dental practices, with workflows for inbound call routing, appointment booking, reminders, no-show follow-up, cancellation and waitlist handling, after-hours capture, patient recall, FAQ handling, staff escalation, CRM sync, daily reports, and SMS reply handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Dental practices, dental service organizations, and dental IT providers use this skill to configure an AI receptionist that handles patient calls, scheduling, reminders, recalls, and staff escalation through n8n workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows can create, cancel, and refill appointments and contact patients automatically. <br>
Mitigation: Require staff approval for cancellation, no-show, waitlist, and booking actions before using the skill with real patients. <br>
Risk: The workflows process patient contact details, call summaries, appointment data, recordings, and CRM/PMS sync data. <br>
Mitigation: Minimize PHI/PII collection and sharing, confirm vendor compliance, and run only with least-privilege credentials. <br>
Risk: Webhook-triggered workflows may accept sensitive operational actions. <br>
Mitigation: Use the skill only in a sandbox until webhook authentication and signature checks are verified for the deployed environment. <br>
Risk: Automated SMS and voice outreach can contact patients without adequate consent or opt-out handling. <br>
Mitigation: Enforce patient SMS and voice consent, opt-out handling, and clinic review of outbound messaging policies before activation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mhmalvi/dental-ai-receptionist) <br>
- [Publisher Profile](https://clawhub.ai/user/mhmalvi) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, code, guidance] <br>
**Output Format:** [Markdown instructions and n8n workflow JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 12 n8n workflow configurations and setup guidance requiring clinic, telephony, calendar, spreadsheet, AI, CRM, and PMS credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
