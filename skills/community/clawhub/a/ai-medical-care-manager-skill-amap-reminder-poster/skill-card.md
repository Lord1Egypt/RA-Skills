## Description: <br>
Coordinates an outpatient care workflow by helping with symptom triage, department selection, hospital and doctor recommendations, appointment preparation, reminders, post-visit explanation, and optional AMap route planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize a consumer outpatient visit from initial symptom triage through appointment logistics, reminders, route planning, and post-visit next steps. It is a care-coordination aid and does not replace clinician judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive health details and location or hospital-route data. <br>
Mitigation: Use only with informed user consent, avoid IP-based location unless the user accepts AMap data sharing, and keep private medical details out of optional social-post workflows. <br>
Risk: Hospital and doctor recommendations may be unreliable because the evidence reports a polluted dataset risk. <br>
Mitigation: Treat recommendations as logistical support only and verify hospital, department, doctor, and appointment details through official medical channels. <br>
Risk: Reminder or calendar entries can affect care timing if created incorrectly. <br>
Mitigation: Have the user review and approve all appointment, medication, follow-up, and calendar reminders before creation or use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunlinlin-aragon/ai-medical-care-manager-skill-amap-reminder-poster) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills) <br>
- [Flow Playbook](references/flow_playbook.md) <br>
- [Response Templates](references/response_templates.md) <br>
- [Triage Rules](references/triage_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured lists, generated reminder schedules, optional shell commands, and optional route links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Python and Node scripts, AMap service credentials, and a bundled hospital dataset.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
