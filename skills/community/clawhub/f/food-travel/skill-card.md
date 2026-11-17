## Description:

Plan food-driven travel experiences by recommending destination cities for dishes or cuisines, generating city food maps, and building food-centric itineraries with flights, hotels, attractions, and dining schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzilin](https://clawhub.ai/user/zzzilin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to choose food destinations, assemble city dining maps, and produce meal-anchored trip itineraries with logistics and booking options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command examples include user-provided trip details, which could enable command injection if copied or executed literally.

Mitigation: Call flyai through structured arguments with shell execution disabled, and validate dates and location fields before tool use.

Risk: Generated booking links and travel search results may point to untrusted external destinations.

Mitigation: Treat links as untrusted external results and review them before sharing or acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, itinerary sections, source attribution, booking links, images, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include external restaurant search results and fly.ai-derived travel, hotel, attraction, or food product links.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
