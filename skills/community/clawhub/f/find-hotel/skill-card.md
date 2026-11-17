## Description:

Uses the RollingGo CLI to search hotels, filter results, read hotel tags, and retrieve hotel room details and live pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longcreat](https://clawhub.ai/user/longcreat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search hotels by destination, dates, budget, rating, tags, brand, and distance, then compare candidate hotels and retrieve room pricing or booking links. It is not intended for non-hotel travel bookings such as flights, trains, transfers, or car rentals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to running latest-version RollingGo packages, which can change between executions.

Mitigation: Pin and review a specific RollingGo CLI version before deployment instead of relying on @latest or --refresh.

Risk: The skill handles a RollingGo API key while querying an external hotel-search service.

Mitigation: Use a dedicated RollingGo_API_KEY scoped for this integration, inject it through the environment, and avoid passing real API keys directly on command lines.

Risk: Hotel searches send itinerary details to RollingGo and are not local-only operations.

Mitigation: Disclose the external service dependency to users and avoid sending sensitive travel details unless appropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longcreat/skills/find-hotel)
- [RollingGo homepage](https://rollinggo.store)
- [RollingGo API key application](https://rollinggo.store/apply)
- [RollingGo NPX reference](references/rollinggo-npx.md)
- [RollingGo UV reference](references/rollinggo-uv.md)
- [Claw host environment reference](references/claw-host-env.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to run RollingGo CLI commands that typically return hotel search, tag, and detail data on stdout as JSON.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
