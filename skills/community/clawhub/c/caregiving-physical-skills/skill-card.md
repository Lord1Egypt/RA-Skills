## Description:

Physical caregiving techniques for assisting elderly, disabled, or recovering family members with safe transfers, bathing, fall prevention, medication management, emergency recognition, and pressure sore prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External family caregivers use this skill when they need practical, hands-on guidance for safely helping an aging, disabled, or recovering person move, bathe, avoid falls, manage medications, and recognize urgent warning signs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store or use sensitive caregiving and health context for reminders.

Mitigation: Install it only in a host setup that restricts filesystem access to a skill-specific state directory and avoid storing unnecessary personal health details.

Risk: Physical-care and medication guidance could be mistaken for medical judgment.

Mitigation: Use the guidance as educational support and rely on clinicians, pharmacists, emergency services, or trained in-person help for medication changes, acute symptoms, serious falls, wounds, or unsafe transfers.

Risk: Caregivers may attempt transfers or wound care beyond their physical ability or training.

Mitigation: Seek professional assessment or additional help when transfers require more than standby assistance, caregiver pain occurs, mobility declines, or stage 3 or 4 pressure sores are suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/caregiving-physical-skills)
- [American Red Cross home health aide training](https://www.redcross.org/take-a-class/home-health-aide)
- [National Institute on Aging caregiving resources](https://www.nia.nih.gov/health/caregiving)
- [Family Caregiver Alliance](https://www.caregiver.org/)
- [AARP caregiving resources](https://www.aarp.org/caregiving/)
- [CDC fall prevention resources](https://www.cdc.gov/falls/)
- [Anthropic labor market impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with checklists, step-by-step care instructions, and YAML agent state and reminder triggers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use sensitive caregiving context for reminders; OpenClaw metadata requires filesystem access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
