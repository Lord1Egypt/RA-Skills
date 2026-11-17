## Description:

One-time setup for ClawCoach AI health coaching. Configures your profile, goals, macro targets, dietary preferences, and coach personality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[authoredniko](https://clawhub.ai/user/authoredniko)

### License/Terms of Use:


## Use Case:

External ClawHub users use this skill to initialize a local ClawCoach health-coaching profile, nutrition goals, macro targets, dietary preferences, allergies, dislikes, and coach persona.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health profile details, goals, allergies, dietary preferences, and meal history are stored as plaintext local JSON files.

Mitigation: Use the skill only on a private account or device, avoid unintended syncing of ~/.clawcoach, and delete that folder when the data should no longer be retained.

## Reference(s):

- [ClawCoach Setup on ClawHub](https://clawhub.ai/authoredniko/skills/clawcoach-setup)
- [Publisher profile](https://clawhub.ai/user/authoredniko)
- [ClawCoach homepage](https://github.com/clawcoach/clawcoach)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational Markdown with local JSON configuration data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local ClawCoach profile and meal-log JSON files under ~/.clawcoach.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
