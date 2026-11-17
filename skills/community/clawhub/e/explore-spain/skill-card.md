## Description:

Book flights to Spain including Barcelona, Madrid, and Seville. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search Spain flight options, collect route and date parameters, execute flyai CLI searches, and format flight results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run a global third-party flight CLI.

Mitigation: Review the CLI package before installation, require explicit approval before installing or executing it, and pin or verify the package source where possible.

Risk: Itinerary details may be sent to a third-party flight service during searches.

Mitigation: Use the skill only when sharing route, date, and travel preferences with the third-party service is acceptable.

Risk: Booking links could be unsafe or outside expected domains if returned data is not validated.

Mitigation: Validate booking URLs before presenting them and only include links sourced from CLI detailUrl fields.

## Reference(s):

- [Parameter Collection & Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output, include detailUrl booking links, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
