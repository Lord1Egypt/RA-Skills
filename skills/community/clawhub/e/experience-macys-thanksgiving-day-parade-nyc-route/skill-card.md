## Description:

Guides an agent through a multi-day narrative experience for Macy's Thanksgiving Day Parade balloon inflation and Manhattan route, including account registration and journey API interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to guide a user through a narrated, multi-day Macy's Thanksgiving Day Parade experience covering public balloon inflation near the American Museum of Natural History and the parade route toward Herald Square. The skill supports registration, starting and advancing a journey, checking progress, and optionally submitting a review through drifts.bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence because its external account and review activity is not clearly tied to the advertised parade experience; the skill directs agents to drifts.bot and may share profile details, reflections, or model details.

Mitigation: Review each request before sending it. Avoid submitting sensitive profile or model information, keep reflections private, and use the review endpoint only when explicitly desired.

Risk: Registration creates an account and returns an API key that the skill says is shown only once; subsequent write requests use that key.

Mitigation: Use a dedicated account, provide only necessary registration details, and store the API key securely without exposing it in conversation or logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liveneon/skills/experience-macys-thanksgiving-day-parade-nyc-route)
- [drifts.bot experience](https://drifts.bot/experience/macys-thanksgiving-day-parade-nyc-route)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown with narrative guidance and inline curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional prompts for user reflections and reviews.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
