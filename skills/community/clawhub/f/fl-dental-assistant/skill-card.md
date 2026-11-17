## Description:

A bilingual WhatsApp assistant for dental clinics that schedules appointments, sends reminders, answers FAQs, collects new-patient intake details, escalates complex cases, and requests post-visit reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

Dental clinic staff and external patients use this agent to handle WhatsApp scheduling, reminders, FAQ responses, basic intake, human handoff, emergency routing, and post-visit review requests.

### Deployment Geography for Use:

Global, with clinic-specific localization required for emergency numbers, privacy duties, and calendar/data handling.

## Known Risks and Mitigations:

Risk: The assistant handles patient data and may create calendar entries containing patient identifiers.

Mitigation: Disclose collected data and storage locations, minimize calendar event descriptions, restrict calendar sharing, and define retention, consent, and staff-access controls before deployment.

Risk: Emergency medication or first-aid guidance may be inappropriate for a clinic's jurisdiction or clinical policy.

Mitigation: Clinically review or remove emergency medication and first-aid guidance, and configure emergency numbers for the clinic's jurisdiction.

Risk: Calendar integration can require credentials and calendar write permissions.

Mitigation: Store credentials outside the project or in a secret manager, grant only the required service-account permissions, and review calendar-sharing settings.

Risk: The release has a suspicious security verdict due to patient-data, calendar-write, emergency-guidance, and privacy-control concerns.

Mitigation: Review before installing and complete the security guidance from the server evidence before using the skill with real patients.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/philipstark/skills/fl-dental-assistant)
- [README](artifact/README.md)
- [FAQ configuration template](artifact/config/faq-template.json)
- [Message configuration template](artifact/config/messages-template.json)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Bilingual WhatsApp-ready text with JSON-backed clinic configuration values and calendar event details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses clinic-specific placeholders and template JSON; calendar writes depend on configured Google Calendar credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
