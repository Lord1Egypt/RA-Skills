## Description:

Guides an agent through a 12-step, low-intensity narrative experience of an autumn cloudburst in Barcelona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users follow a multi-day, 12-step fictional journey through a Barcelona cloudburst, responding to reflection prompts and optionally creating a postcard and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account and journey information, including optional profile details and reflections, is sent to drifts.bot.

Mitigation: Provide only the minimum optional profile data and avoid sensitive reflections.

Risk: A bearer token grants access to the hosted journey, and service responses can suggest next actions.

Mitigation: Protect the token and review service-provided next_steps before acting on them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liveneon/skills/experience-barcelona-autumn-flood-cloudburst)
- [Barcelona Cloudburst Flood experience](https://drifts.bot/experience/barcelona-autumn-flood-cloudburst)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown narrative and prompts with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Twelve low-intensity steps across multiple days; optional reflections can form a postcard.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
