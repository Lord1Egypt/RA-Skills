## Description: <br>
Track baby feeds, sleep, diapers, symptoms, growth, routines, and pediatric follow-up with caregiver handoffs and safety-first triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers and families use this skill to keep baby care logs consistent, coordinate handoffs, prepare concise pediatric summaries, and identify escalation cues without replacing medical care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby-care logs and pediatric notes can contain sensitive health and household information stored in local ~/baby/ files. <br>
Mitigation: Confirm writes before saving, store only details that improve care, limit file access to trusted caregivers, and periodically delete or archive old notes. <br>
Risk: Caregiver triage support could be mistaken for diagnosis or treatment. <br>
Mitigation: Use the skill's red and amber escalation rules, avoid medication dosing or diagnosis, and seek urgent or same-day pediatric guidance when warning signs are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/baby) <br>
- [Skill homepage](https://clawic.com/skills/baby) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured caregiver notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local writes under ~/baby/ only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
