## Description:

Baby Guide provides month-based baby care reference guidance for developmental milestones, complementary feeding, early education, vaccination reminders, and common symptom handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill as a general baby-care reference for age-based growth milestones, feeding guidance, early education activities, vaccination reminders, and common symptom checklists. It should not be used as a substitute for pediatric medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat high-stakes pediatric guidance as diagnosis, medication advice, emergency triage, vaccine timing, allergy advice, or feeding-problem advice.

Mitigation: Use the skill only as general reference material and consult a qualified clinician for diagnosis, medication decisions, emergencies, vaccine schedules, allergies, or feeding problems.

Risk: The bundled design helper can write command arguments to a local history file under the baby-guide data directory.

Mitigation: Review local data handling before use, avoid passing sensitive information to helper commands, and disable or remove history logging if it is not needed.

Risk: The authoritative security verdict flags the release as suspicious and requiring review before installation.

Mitigation: Review and scan the skill before deployment, with particular attention to the baby-care guidance and local history logging behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes general baby-care reference text and command-driven checklist output; not suitable for clinical decision-making.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
