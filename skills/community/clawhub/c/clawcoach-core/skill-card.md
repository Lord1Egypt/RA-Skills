## Description:

AI health coach with dual personality modes (Supportive Mentor or Savage Roaster). Tracks nutrition from food photos, provides data-driven coaching, and holds you accountable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[authoredniko](https://clawhub.ai/user/authoredniko)

### License/Terms of Use:


## Use Case:

External users use this skill as a conversational health coach to track meals, review daily calories and macros, receive meal suggestions, and choose between supportive or accountability-focused coaching personas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal profile and food-log data locally in ~/.clawcoach/.

Mitigation: Review the local data directory before installation and avoid entering information that should not be retained on the device.

Risk: The Savage Roaster persona uses blunt accountability humor that may not suit every user.

Mitigation: Use the Supportive Mentor persona when a gentler tone is preferred, and rely on the built-in limits against body-image, distress-related, or discriminatory mocking.

Risk: The listed distress and eating-disorder support numbers are United States resources.

Mitigation: Users outside the United States should identify appropriate local emergency or crisis resources before relying on the skill for support guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/authoredniko/skills/clawcoach-core)
- [ClawCoach homepage](https://github.com/clawcoach/clawcoach)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown conversational responses with local JSON profile and food-log updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses concise coaching replies, shows calories and macros, and may update persona and local profile state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
