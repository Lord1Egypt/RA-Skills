## Description: <br>
Book flights to Canada including Vancouver, Toronto, and Montreal, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel guidance powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel agents use this skill to search Canada travel options, especially flights to Vancouver, Toronto, and Montreal, by executing flyai CLI searches and formatting current booking results with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to install an unpinned global npm package before travel searches. <br>
Mitigation: Install and vet the flyai CLI separately in an isolated environment, pin an approved package version, and require user confirmation before any package installation. <br>
Risk: Travel route, date, and preference data may be sent to flyai or Fliggy services during searches. <br>
Mitigation: Review data-sharing expectations with the user before execution and avoid sending sensitive personal details unless necessary for the requested search. <br>
Risk: Booking links can lead to external purchase flows. <br>
Mitigation: Require explicit user confirmation before opening booking links or taking actions beyond presenting search results. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Explore Canada ClawHub Release](https://clawhub.ai/dingtom336-gif/explore-canada) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include detailUrl booking links when options are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
