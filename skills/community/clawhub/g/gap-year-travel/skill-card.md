## Description: <br>
Book flights for gap year travel and year-off adventures, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel needs powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search current gap-year and long-term travel options, compare flight results, and present bookable itineraries with live CLI-sourced booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install and run a global third-party travel CLI before answering. <br>
Mitigation: Review the CLI package first, prefer installing it manually or in a sandbox, and confirm commands before execution. <br>
Risk: Flight and booking guidance can be misleading if the agent answers from prior knowledge instead of current CLI output. <br>
Mitigation: Require current flyai CLI output with booking links for listed results, and stop or ask the user to retry when the CLI cannot provide valid results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/gap-year-travel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight-search summaries with comparison tables, booking links, and inline shell commands when installation or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are expected to use flyai CLI results and include a booking link for each listed result when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
