## Description: <br>
Book flights with airport hotel recommendations for layovers and early departures, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and related travel searches powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to collect route details, run live FlyAI travel searches, and present bookable flight or airport-hotel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute an unpinned third-party CLI. <br>
Mitigation: Require user approval before installation, prefer a pinned or sandboxed install, and verify the package source before running commands. <br>
Risk: Travel search details may be sent to the FlyAI provider. <br>
Mitigation: Confirm user intent and avoid submitting sensitive or unnecessary personal details in CLI queries. <br>
Risk: Ambiguous travel requests can produce incorrect routes, dates, or booking options. <br>
Mitigation: Ask clarifying questions for missing origin, destination, or date before running searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/airport-hotel) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output and booking detailUrl links; raw JSON should not be returned.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
