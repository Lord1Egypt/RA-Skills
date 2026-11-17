## Description:

Dad.skill is a parenting co-pilot for fathers that summarizes daily child-care updates, coordinates family schedules, tracks bonding moments, suggests age-appropriate activities, and reminds users it is not medical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External parents, especially fathers and co-parents, use this skill to stay current on locally logged child-care routines, coordinate schedules and night shifts, and record bonding moments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive child and family notes locally where other users of the same agent environment may be able to read them.

Mitigation: Install it only in environments where agent users are allowed to see the family notes, and remove ~/.dad-skill/family/ to delete the stored data.

Risk: Broad activation phrases and night-mode behavior may cause the skill to respond during casual parenting questions.

Mitigation: Use explicit invocation habits for briefings, schedule checks, bonding logs, night shift questions, and activity suggestions.

Risk: Child-care guidance could be mistaken for medical advice.

Mitigation: Treat responses as practical family coordination only and consult a pediatrician for illness, diagnosis, treatment, or health concerns.

## Reference(s):

- [Age-Appropriate Activities Reference](references/age-activities.md)
- [Dad's Bonding Log Template](templates/DAD-LOG.md)
- [Dad.skill on ClawHub](https://clawhub.ai/realteamprinz/skills/dad)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text with local JSONL and Markdown note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local family notes under ~/.dad-skill/family/ and does not transmit data externally according to the artifact.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
