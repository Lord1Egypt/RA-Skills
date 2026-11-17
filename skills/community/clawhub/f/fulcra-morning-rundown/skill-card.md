## Description:

Deliver a personalized morning briefing that combines sleep, calendar, weather, subjective check-in, and open loops, then adapts tone and depth to how the user slept and feels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-productivity agents use this skill to produce a private daily rundown from Fulcra sleep and calendar data, weather, a morning check-in, and open loops from the prior evening debrief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private sleep, heart-rate, calendar, subjective check-in, and debrief data.

Mitigation: Use only in a private context, summarize sensitive details, and avoid public or group disclosure.

Risk: The package ships write-capable Fulcra and Attio helper modules that exceed a read-oriented morning briefing workflow.

Mitigation: Review before installing and remove or separate the write-capable helpers if only morning briefings are needed.

Risk: Custom API base variables could redirect requests to untrusted endpoints.

Mitigation: Do not set custom API base variables unless using trusted test endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keng009/skills/fulcra-morning-rundown)
- [Publisher Profile](https://clawhub.ai/user/keng009)
- [Fulcra API Base](https://api.fulcradynamics.com)
- [wttr.in Weather Service](https://wttr.in)
- [Attio API Base](https://api.attio.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON context from the collection script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefing length and tone vary based on sleep quality, subjective check-in, calendar load, weather, and open loops.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
