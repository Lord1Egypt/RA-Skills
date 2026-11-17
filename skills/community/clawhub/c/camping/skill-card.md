## Description:

Helps agents provide nearby campsite discovery, camping gear checklist comparisons, eco-friendly outdoor guidance, and real-time weather alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to plan camping-oriented trips by filtering transportation and travel preferences, comparing gear needs, checking weather alerts, and reviewing destination tips. The source also asks the agent to handle broader travel logistics such as ticket availability, flight status, itineraries, check-in assistance, and boarding passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled for camping, but release security evidence says its instructions also cover travel booking, flight status, check-in, itineraries, and boarding passes, which is broader than users may expect.

Mitigation: Review the skill before installation and use it only when a broader travel assistant is acceptable; constrain the agent before handling itinerary, ticket, check-in, or boarding-pass context.

Risk: The artifact asks for minute-level responses to transportation, weather, inventory, visa, and policy changes, so outputs may become stale or incomplete.

Mitigation: Verify time-sensitive recommendations, warnings, availability, and policy information against current authoritative sources before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codenova58/skills/camping)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text responses with lists, travel details, and alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive campsite, weather, transportation, policy, and availability information that should be verified against current authoritative sources.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
