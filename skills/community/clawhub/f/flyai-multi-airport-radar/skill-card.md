## Description:

同城不同价 is a multi-airport fare comparison agent that expands a traveler's departure airport and date options, builds a price matrix, and compares airfare with cross-city transportation costs to identify lower-cost itineraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to compare nearby departure airports, flexible departure dates, and cross-city transportation costs before choosing a flight itinerary. It can also suggest related hotel and attraction booking links when relevant travel data is returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests global or sudo installation of an unpinned latest CLI package.

Mitigation: Install only after review, avoid sudo/global latest installs, and pin one verified CLI package version.

Risk: The workflow includes a TLS-bypass environment variable for flight searches.

Mitigation: Preserve HTTPS certificate validation and remove TLS-bypass commands before use.

Risk: The skill stores travel preferences and household details in memory or a local profile file.

Mitigation: Enable persistent profile storage only with explicit user opt-in, keep stored fields minimal, and provide clear deletion controls.

Risk: The skill can surface booking links from returned travel-search data.

Mitigation: Validate booking-link domains and limit outputs to the requested flight comparison and related travel options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-multi-airport-radar)
- [SKILL.md](artifact/SKILL.md)
- [Workflow](artifact/reference/workflow.md)
- [Flight Search Reference](artifact/reference/search-flight.md)
- [Train Search Reference](artifact/reference/search-train.md)
- [Hotel Search Reference](artifact/reference/search-hotel.md)
- [POI / Attraction Search Reference](artifact/reference/search-poi.md)
- [User Profile Storage](artifact/reference/user-profile-storage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, itinerary summaries, inline booking links, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include price matrices, route tradeoff analysis, travel-profile prompts, and links returned by travel search tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
