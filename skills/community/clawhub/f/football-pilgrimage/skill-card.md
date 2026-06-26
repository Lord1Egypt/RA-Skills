## Description: <br>
Generates narrative football pilgrimage guides for football teams, including stadium tours, museums, fan pubs, cultural landmarks, On This Day history, trip match detection, and ticket search guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isgaoyun](https://clawhub.ai/user/isgaoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to build football-focused trip guides for a selected team, combining club history, stadium experiences, local fan culture, match schedule checks, and optional ticket, flight, and hotel searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send team names, travel dates, departure city, and ticket or travel intent to external lookup services including ESPN, web search, and flyai. <br>
Mitigation: Use the skill only when those details can be shared with external services, and avoid providing departure city or exact travel dates unless travel, ticket, flight, or hotel lookup is desired. <br>
Risk: Schedules, ticket availability, prices, opening hours, and travel options can change after the guide is generated. <br>
Mitigation: Verify match schedules, attraction details, prices, and tickets through official sources before booking or traveling. <br>
Risk: Historical On This Day content and spot backstories can be misleading if unsupported by search results. <br>
Mitigation: Include only events and stories grounded in retrieved search results, omit unsupported dates, and perform an extra verification search when a historical claim is uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isgaoyun/football-pilgrimage) <br>
- [Commands Reference](references/commands.md) <br>
- [Data Coverage](references/data-coverage.md) <br>
- [ESPN API Reference](references/espn-api.md) <br>
- [Examples](references/examples.md) <br>
- [Guide Structure](references/guide-structure.md) <br>
- [Response Schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel guide with structured sections, sourced recommendations, optional image links, and optional shell-style flyai or curl commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors the user's language and may include match alerts, itinerary phases, spot stories, On This Day entries, and ticket or travel search guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
