## Description:

Helps an agent diagnose, rescue, and execute cooking tasks with practical guidance on heat control, seasoning, doneness, timing, substitutions, equipment, and food safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for real-time cooking assistance: rescuing dishes, choosing technique adjustments, answering temperature, timing, and safety questions, adapting substitutions, and sequencing a meal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain local long-term memory about the user's kitchen, meals, guests, allergies, intolerances, and food constraints.

Mitigation: Install only when the user is comfortable with that local memory behavior and review the configured Clawic data folders.

Risk: The skill may read and edit shared health and contacts notes used by other skills.

Mitigation: Prefer explicit confirmation before saving or deleting health or contact records, and review ~/Clawic/data/health/ and ~/Clawic/data/contacts/ after installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/cooking)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic Cooking skill page](https://clawic.com/skills/cooking)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational Markdown with optional local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update local Clawic cooking, health, and contacts notes when installed and invoked.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
