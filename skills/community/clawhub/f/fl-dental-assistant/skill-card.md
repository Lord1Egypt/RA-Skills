## Description: <br>
Dental Clinic Assistant is a bilingual WhatsApp virtual receptionist for dental clinics that schedules appointments, sends reminders, answers FAQs, collects new-patient intake details, routes urgent cases, and requests post-visit reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External dental clinic staff use this skill to automate routine WhatsApp reception workflows, including appointment booking, rescheduling, reminders, FAQ responses, new-patient intake, review requests, and staff handoff. It is intended for clinic-approved deployment with local privacy, consent, emergency, and credential controls in place. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles patient data through WhatsApp intake, staff alerts, and calendar event descriptions. <br>
Mitigation: Deploy only with clinic and legal approval, add explicit patient privacy and consent wording before intake, and avoid unnecessary patient details in calendar events or staff alerts. <br>
Risk: The skill can create, cancel, or reschedule appointments. <br>
Mitigation: Require stronger patient verification before cancellations or rescheduling and keep staff review available for disputed or uncertain changes. <br>
Risk: Emergency responses and phone numbers may be region-specific and could create patient safety risk if misconfigured. <br>
Mitigation: Configure emergency numbers by clinic region and remove or require clinician review for emergency advice before production use. <br>
Risk: Google Calendar integration depends on service-account credentials. <br>
Mitigation: Use a dedicated limited Google Calendar or service account, protect credential files, and rotate credentials when access changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PhilipStark/fl-dental-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/PhilipStark) <br>
- [Google Calendar API Setup](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational WhatsApp response text plus JSON configuration templates and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Portuguese response templates for clinic-facing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
