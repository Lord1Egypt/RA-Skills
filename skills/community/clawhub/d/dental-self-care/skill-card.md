## Description:

Helps users maintain oral health routines, track dental symptoms and supplies, find lower-cost care options, and prepare communication scripts while emphasizing escalation to licensed dental or emergency care for urgent symptoms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users who lack regular access to dental care use this skill to plan preventive oral hygiene, maintain symptom and supply trackers, identify affordable provider options, and draft appointment or payment-plan outreach. It is informational support and should not replace licensed dental or emergency medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DIY dental or emergency instructions may be mistaken for licensed dental or medical care.

Mitigation: Use the skill for reminders, supply lists, provider research, and preparation only; escalate urgent symptoms to a licensed dentist, urgent-care facility, or emergency department.

Risk: Symptom, income, location, and contact details may be stored in local tracker files.

Mitigation: Use a controlled file location with appropriate permissions, retention, and deletion practices before allowing the skill to persist sensitive details.

Risk: Provider outreach scripts may include sensitive health or financial information.

Mitigation: Review and edit all generated messages before sending, and include only the minimum personal information needed for the specific provider interaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/dental-self-care)
- [ClawHub publisher profile](https://clawhub.ai/user/howtousehumans)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with checklists, decision trees, tracker tables, communication scripts, reminders, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local filesystem trackers for symptoms, supplies, adherence, and provider outreach.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
