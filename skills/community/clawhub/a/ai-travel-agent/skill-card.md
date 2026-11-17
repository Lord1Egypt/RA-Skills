## Description:

AI Travel Agent helps users plan single-destination and multi-stop trips by searching SerpAPI-backed flight, hotel, and transport options, recommending travel dates and destinations, and optionally integrating with calendar skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[floogles](https://clawhub.ai/user/floogles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect trip preferences, search flights, hotels, and internal transport, compare itinerary options, and produce costed trip plans with booking links but no booking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if commands are run with `--key $SERPAPI_KEY` as shown in parts of the skill instructions.

Mitigation: Use the SERPAPI_KEY environment variable or the documented credential files, and avoid passing the key as a command-line argument.

Risk: Optional calendar access could expose availability data if used before the user has clearly chosen a date-range or calendar action.

Mitigation: Allow calendar access only after explicit user confirmation for date suggestions or calendar-event creation.

Risk: Travel search results may be incomplete, stale, or differ from booking-site terms.

Mitigation: Treat itinerary options as planning guidance and confirm price, availability, baggage, cancellation, and booking terms on the linked provider before purchase.

## Reference(s):

- [AI Travel Agent ClawHub Page](https://clawhub.ai/floogles/skills/ai-travel-agent)
- [SerpAPI](https://serpapi.com)
- [SerpAPI Reference](references/serpapi.md)
- [Seasonal Destination Guide](references/seasonal-destinations.md)
- [Multi-Stop Route Templates](references/multi-stop-routes.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON search-result data from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces itinerary summaries, comparison tables, booking links, and optional calendar-event guidance; it does not book travel.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
