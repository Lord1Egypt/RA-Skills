## Description:

Helps agents guide outpatient care tasks, including symptom triage, department and hospital recommendations, appointment preparation, reminders, post-visit explanations, and optional AMap route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to move through an outpatient visit workflow: triage symptoms, choose a likely department, prepare for an appointment, generate reminders, plan a route, and summarize post-visit next steps. It is intended for workflow support and plain-language explanation, not medical diagnosis.

### Deployment Geography for Use:

China, with Beijing-specific registration defaults

## Known Risks and Mitigations:

Risk: Sensitive health or location details may be sent to AMap for hospital directions.

Mitigation: Ask for explicit user confirmation before using route planning, share only the minimum location and destination details needed, and offer manual map-search guidance when the user does not want to share location data.

Risk: Reminder or calendar entries may be created from appointment, medication, follow-up, inspection, or pickup times.

Mitigation: Preview the exact reminder content and timing and require confirmation before creating entries or asking another tool to create them.

Risk: Medication schedules extracted from user text may be incomplete or misunderstood.

Mitigation: Treat generated medication reminders as adherence aids only, ask the user to confirm them against the clinician's prescription, and avoid changing dose, frequency, duration, or stop/start decisions.

Risk: Triage and hospital or department recommendations could be mistaken for a diagnosis or emergency assessment.

Mitigation: State that outputs do not replace medical judgment, prioritize emergency guidance for high-risk symptoms, and avoid normal outpatient recommendations when emergency signals are present.

Risk: Optional social-sharing content could expose private medical details.

Mitigation: Use the social-sharing handoff only when the user explicitly asks for it, preview the content, and remove or generalize private health, location, and appointment details unless the user approves inclusion.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/sunlinlin-aragon/skills/ai-medical-care-manager-skill-amap-reminder-poster)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)
- [Flow playbook](references/flow_playbook.md)
- [Triage rules](references/triage_rules.md)
- [Response templates](references/response_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and structured reminder, triage, route, or preparation-card data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Python and Node scripts, local hospital data, and optional AMap credentials to produce route links and reminder lists.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
