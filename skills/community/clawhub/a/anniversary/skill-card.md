## Description: <br>
Book anniversary trip flights, romantic getaways and couple travel with celebration flight deals, including flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search and compare anniversary travel options, especially couple-friendly flights and romantic getaway itineraries. The skill guides an agent to collect trip parameters, run the flyai CLI, and format bookable results with real-time booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and rely on a globally installed external flyai CLI. <br>
Mitigation: Review the CLI package and installation policy before use, and run it only in an approved environment. <br>
Risk: Travel requests and raw CLI activity may be retained locally in .flyai-execution-log.json. <br>
Mitigation: Disable local execution-log creation where possible, or redact and delete logs containing travel details after use. <br>
Risk: Travel answers can be misleading if the agent bypasses live CLI results or omits booking links. <br>
Mitigation: Require output validation that every displayed result comes from flyai CLI data and includes a detailUrl booking link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/anniversary) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include bookable detail links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
