## Description:

Help users find their ideal travel destination through personalized recommendations based on structured needs assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkingzq](https://clawhub.ai/user/walkingzq)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want an agent to collect travel preferences conversationally and recommend one well-matched destination with rationale, itinerary guidance, and traveler-facing references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require third-party FlyAI and Xiaohongshu-style lookups while producing destination advice.

Mitigation: Allow those lookups only when they are needed for the recommendation, and avoid sharing detailed travel history or stored profile location unless the user explicitly provides it for the trip.

Risk: The artifact includes behavior that may repair PATH settings, source shell profiles, or install a global npm package to enable FlyAI.

Mitigation: Require explicit user approval before shell profile sourcing, PATH repair, or global npm installation, and review any generated shell command before execution.

Risk: FlyAI links may point to third-party commercial travel content.

Mitigation: Present these links as external commercial references and have the user verify price, availability, and terms before relying on them.

## Reference(s):

- [FlyAI Integration Guide](references/flyai-integration.md)
- [Questionnaire Guide](references/questionnaire-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/walkingzq/skills/destination-finder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendation with conversational questions, structured itinerary sections, source links, and inline shell commands when FlyAI lookup is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party travel links, traveler feedback summaries, and image or booking URLs returned by approved lookup tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
