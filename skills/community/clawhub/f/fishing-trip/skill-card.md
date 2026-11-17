## Description:

Book flights for fishing trips to prime angling destinations, with additional travel-planning support for hotels, trains, attractions, itineraries, visa information, travel insurance, and car rental through Fliggy-powered flyai results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search flight options for fishing trips, compare recommended, cheapest, fastest, or direct routes, and return booking-ready Markdown based on flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm package and run a third-party travel CLI.

Mitigation: Review installation steps before use, prefer explicit install approval, and pin package versions in controlled environments.

Risk: Travel search details may be sent to a third-party provider and returned with mandatory booking links.

Mitigation: Use only in environments where sharing travel-search inputs with the provider and presenting external booking links is acceptable.

Risk: Command templates may be unsafe if user-supplied travel parameters are passed through a shell without validation.

Mitigation: Validate origin, destination, dates, and sort options, and prefer non-shell argument execution where supported.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables with CLI-derived travel results, booking links, and supporting shell commands when setup or retry steps are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must come from flyai CLI output and include booking links when flight options are presented.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
