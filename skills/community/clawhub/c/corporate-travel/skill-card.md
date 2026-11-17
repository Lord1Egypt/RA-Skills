## Description:

Book corporate travel flights for company trips and enterprise travel, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and related travel tasks powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and travel coordinators use this skill to search corporate travel routes, collect flight parameters, run FlyAI flight-search commands, and present policy-aware booking options with required booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require a persistent global npm installation of an unpinned flyai CLI.

Mitigation: Use a pinned, reviewed, sandboxed CLI installation and require explicit user approval before installing or running it.

Risk: Flight-search details are sent to an external travel-search service.

Mitigation: Confirm user consent before transmission and avoid adding sensitive itinerary or traveler details beyond what the CLI command needs.

Risk: Shell-style commands are built from user-derived route, date, and preference inputs.

Mitigation: Use only documented flyai parameters, quote user-provided values, and reject unsupported flags instead of inventing parameters.

Risk: Booking links influence travel purchasing decisions.

Mitigation: Only display results that include a CLI-provided detailUrl and remind users to follow their company travel policy before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/corporate-travel)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when installation or execution steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output and each included result must include a detailUrl booking link.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
