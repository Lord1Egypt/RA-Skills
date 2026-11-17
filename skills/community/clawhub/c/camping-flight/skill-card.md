## Description:

Book flights for camping and glamping trips to outdoor destinations, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and related travel planning powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill through compatible agents to search flight options for camping or glamping trips, compare route choices by recommended, cheapest, fastest, or direct preferences, and receive CLI-backed booking results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run a third-party FlyAI/Fliggy CLI globally.

Mitigation: Review and install the CLI from a trusted source yourself, pin or review the package version, and confirm consent before use.

Risk: Unvalidated user travel text could be passed into shell commands.

Mitigation: Map user input only to documented parameters, quote command arguments, and avoid passing raw user text directly to the shell.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown comparison tables and recommendations with booking links, supported by inline shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLI-derived results and detailUrl booking links; raw JSON output is not intended for users.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
