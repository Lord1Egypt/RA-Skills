## Description:

Generate a football pilgrimage guide for any team, covering stadium tours, football museums, fan pubs, cultural landmarks, date-matched historic football events, trip-date match detection, and ticket search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isgaoyun](https://clawhub.ai/user/isgaoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to create football-focused travel guides for a selected club, combining club history, stadium and fan-culture stops, trip-date match checks, and optional travel or ticket lookup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may construct shell-style ticket, flight, hotel, or API commands from user-provided and web-sourced values.

Mitigation: Use structured tool invocations or validate and quote all command arguments before execution.

Risk: The skill can surface third-party booking links or travel options that may request sensitive travel or payment details.

Mitigation: Confirm the provider, destination, event, and booking context before sharing or entering sensitive information.

Risk: Football history and On This Day narratives can become misleading if events are filled from memory rather than retrieved evidence.

Mitigation: Include only events found in search results and omit days where no supported event is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isgaoyun/skills/football-pilgrimage)
- [ESPN API Reference](artifact/references/espn-api.md)
- [Guide Structure](artifact/references/guide-structure.md)
- [Data Coverage](artifact/references/data-coverage.md)
- [Response Schemas](artifact/references/schemas.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown narrative guide with structured sections, source-backed football history, optional ticket and travel lookup commands, and supporting JSON-shaped response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mirrors the user's language and omits date-specific historic events when they are not supported by search results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
