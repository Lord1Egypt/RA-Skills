## Description:

An outpatient care workflow assistant that triages symptoms, suggests departments and top hospital/doctor matches, guides appointment booking, prepares visit cards and reminders, explains post-visit materials, and can plan AMap routes to the hospital.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage a complete outpatient visit workflow, from symptom triage and department selection through booking preparation, reminders, route planning, and post-visit explanation. It is an operational care-navigation aid and should not be used as a substitute for clinical diagnosis, emergency assessment, or official hospital confirmation.

### Deployment Geography for Use:

China, with Beijing-specific hospital data and booking guidance.

## Known Risks and Mitigations:

Risk: Sensitive healthcare-route location data may be sent to AMap during IP geolocation, geocoding, or route planning.

Mitigation: Require explicit user consent before using IP geolocation or sending addresses/coordinates to AMap, and prefer a coarse origin instead of a home address when that is sufficient.

Risk: Hospital, department, or doctor recommendations may be affected by polluted provider data.

Mitigation: Ask users to verify recommended doctors, departments, schedules, and booking availability through official hospital or registration channels before acting.

Risk: Users may over-rely on the skill for diagnosis or emergency decisions.

Mitigation: Present outputs as care-navigation support only, prioritize emergency care for high-risk symptoms, and state that the skill does not replace clinicians or emergency services.

Risk: AMap credentials could be exposed if stored in local plaintext configuration.

Mitigation: Keep the AMap Web Service key in environment configuration and avoid pasting credentials into prompts, logs, or generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunlinlin-aragon/skills/ai-medical-care-manager)
- [OpenClaw Skill Documentation](https://docs.openclaw.ai/skills)
- [Care Flow Playbook](references/flow_playbook.md)
- [Triage Rules](references/triage_rules.md)
- [Response Templates](references/response_templates.md)
- [AMap Web Service API](https://restapi.amap.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON outputs from helper scripts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python and Node.js scripts; AMap route features require an AMap Web Service key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
