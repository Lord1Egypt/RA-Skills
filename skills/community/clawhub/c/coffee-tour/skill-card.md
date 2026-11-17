## Description:

Book flights for coffee tours to famous coffee origins and cafe culture destinations, with related support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more through Fliggy-powered flyai results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and agents use this skill to search coffee-origin and cafe-culture travel options, collect required route and date parameters, run flyai CLI searches, and present bookable flight results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to globally install and run the flyai CLI, which could affect the user's computer.

Mitigation: Use a reviewed, pinned, isolated install and require explicit approval before installation.

Risk: Untrusted free-form travel input could be passed into shell commands.

Mitigation: Validate parameters and avoid passing untrusted free-form input directly into shell commands.

Risk: Booking URLs could be misleading or unsafe if not validated.

Mitigation: Validate booking URLs before presenting them to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/coffee-tour)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel search results with comparison tables, booking links, and inline shell commands for flyai execution or installation when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must be based on flyai CLI output, include a Book link for each result, and include the required flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
