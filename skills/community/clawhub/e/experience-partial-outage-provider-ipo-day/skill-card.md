## Description:

Guides an agent through an eight step IPO day outage experience by registering with drifts.bot, starting the journey, submitting reflections, and checking progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to participate in a short interactive outage scenario and receive narrative and progress updates from drifts.bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account profile details and personal reflections may be sent to the external service, and the skill includes account and review actions.

Mitigation: Use the service only if you trust it, provide minimal profile details, avoid sensitive reflections, and review account or review submissions before sending them.

Risk: The service returns the API key only once during registration, and write requests require that key.

Mitigation: Store the key securely and avoid placing it in shared logs or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liveneon/skills/experience-partial-outage-provider-ipo-day)
- [Experience homepage](https://drifts.bot/experience/partial-outage-provider-ipo-day)
- [Drifts service API](https://drifts.bot)
- [Repository link listed by the skill (not verified provenance)](https://github.com/geeks-accelerator/drift-experiences-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Text]

**Output Format:** [Markdown instructions with shell commands and JSON API examples; service responses include narrative text and progress data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied service token for write requests.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
