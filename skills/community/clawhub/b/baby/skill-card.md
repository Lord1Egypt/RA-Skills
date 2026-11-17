## Description:

Track baby feeds, sleep, diapers, symptoms, growth, routines, and pediatric follow-up with caregiver handoffs and safety-first triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers use this skill to keep baby care logs consistent across feeds, sleep, diapers, symptoms, medications, growth, routines, and appointments. It helps prepare caregiver handoffs and pediatric-ready summaries while keeping triage support within escalation and documentation scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create local notes containing sensitive child health and caregiver information.

Mitigation: Use it only on a trusted device and account, keep only care coordination details, and review or delete ~/baby/ files when they are no longer needed.

Risk: Triage support could be mistaken for diagnosis or treatment.

Mitigation: Use it to organize observations and escalation cues only; seek urgent local care for red alerts and same-day pediatric guidance for amber patterns.

Risk: Incomplete timestamps, units, or caregiver handoffs can make summaries less useful for pediatric review.

Mitigation: Record observed facts with times, units, baseline changes, and clearly marked missing fields before relying on summaries for visits or calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/baby)
- [Skill Homepage](https://clawic.com/skills/baby)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and concise caregiver-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local note files under ~/baby/ after user confirmation; no external network requests by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
