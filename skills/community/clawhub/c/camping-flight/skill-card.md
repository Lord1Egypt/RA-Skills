## Description: <br>
Book flights for camping and glamping trips to outdoor destinations, with additional travel support for hotels, trains, attraction tickets, itineraries, visa information, travel insurance, and car rental powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel assistants use this skill to search and compare camping or glamping flight options through flyai CLI results, then present bookable Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to globally install and run the external @fly-ai/flyai-cli package. <br>
Mitigation: Approve installation manually, verify or pin the package before use, and review generated commands before execution. <br>
Risk: Broad travel-query triggers may run flight search commands for ambiguous or non-camping requests. <br>
Mitigation: Confirm origin, destination, and travel intent before command execution, especially for non-camping or ambiguous travel requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/camping-flight) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight search results with comparison tables, booking links, and inline CLI commands when setup or recovery is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output and include booking links when flight options are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
