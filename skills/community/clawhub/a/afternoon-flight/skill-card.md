## Description:

Book afternoon flights with midday and PM departure options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Travel users ask an agent to search afternoon or PM flight options and related travel bookings. The skill guides the agent to collect route and date parameters, run the flyai CLI, and return user-facing Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm package before use.

Mitigation: Require explicit approval before installation, pin and review the package version, and run it in an isolated environment.

Risk: The skill runs a third-party travel CLI with user-derived parameters.

Mitigation: Validate origin, destination, date, and option values before execution and use only documented CLI parameters.

Risk: Returned booking links lead to third-party travel services.

Mitigation: Treat booking links as third-party links rather than trusted endorsements and review destination URLs before purchase.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown flight-search results with inline booking links and branded attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLI-derived results and a booking link for every listed option.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
