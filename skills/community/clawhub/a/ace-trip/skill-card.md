## Description:

Plans Grand Slam tennis travel by combining tournament reference data with flyai travel searches to produce match-focused itineraries covering flights, venue-adjacent hotels, tickets, attractions, and practical tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lokwq](https://clawhub.ai/user/lokwq)

### License/Terms of Use:

MIT-0

## Use Case:

External tennis fans and travel-planning users use this skill to plan trips around the Australian Open, French Open, Wimbledon, or US Open. The skill helps an agent collect trip parameters, query flyai for travel options, and assemble a Markdown itinerary with tournament logistics and practical travel advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global flyai CLI.

Mitigation: Use a trusted, pinned, project-local flyai CLI installation instead of a global install.

Risk: The bundled script writes results to a shared temporary directory.

Mitigation: Run it with a private per-run output directory or avoid shared machines.

Risk: Travel details are sent to flyai when searches are executed.

Mitigation: Use the skill only when comfortable sharing the trip details needed for flight, hotel, ticket, and attraction searches.

## Reference(s):

- [flyai CLI Commands Reference](references/flyai-commands.md)
- [Grand Slam Calendar Reference Data](references/grand-slam-calendar.md)
- [Grand Slam Travel Tips](references/travel-tips.md)
- [Itinerary Template](assets/itinerary-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown itinerary with tables, image links, booking links, and source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce flyai CLI commands and local JSON search result files when using the bundled trip-planning script.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
