## Description:

Book flights to the UK including London, Edinburgh, and Manchester, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents, developers, and end users can use this skill to search UK travel options through the flyai CLI and format real-time flight results with booking links. It is intended for UK-related flight searches and adjacent travel planning tasks such as hotels, trains, attractions, insurance, and car rental.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require installing and running an unpinned global npm package.

Mitigation: Install only in a trusted or isolated environment, review and pin the flyai CLI package before use, and approve global package installation deliberately.

Risk: Unsafe shell-style command templates or untrusted travel data can produce misleading booking guidance.

Mitigation: Use the scanner guidance: verify CLI output, booking URLs, and provider branding before relying on results or entering payment or sensitive travel details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/palexu/skills/explore-uk)
- [Provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output and booking links for included travel results.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
