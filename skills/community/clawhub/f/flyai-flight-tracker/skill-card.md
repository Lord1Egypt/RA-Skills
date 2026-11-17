## Description:

Track flight prices across a date range, show day-by-day comparison charts to identify trends and booking windows, and support related Fliggy-powered travel workflows including flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to run flyai CLI searches, compare flight prices across date ranges, and present booking-window guidance with booking links. It can also guide related Fliggy-powered travel workflows such as hotels, train tickets, attractions, itinerary planning, visa information, insurance, and car rental.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned global third-party npm CLI and may send itinerary details such as cities and dates to the flyai/Fliggy service.

Mitigation: Review before installing, prefer a pinned CLI version, request explicit approval before installation, and use a sandboxed or project-local install path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/flyai-flight-tracker)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results and booking links; raw JSON is not an intended output.]

## Skill Version(s):

v3.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
