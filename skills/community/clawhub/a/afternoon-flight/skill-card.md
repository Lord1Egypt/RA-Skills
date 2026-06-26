## Description: <br>
Book afternoon flights with midday and PM departure options, with additional support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agents use this skill to search afternoon and related travel options through the flyai CLI, compare returned results, and present booking links in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the third-party flyai CLI. <br>
Mitigation: Require manual approval before any npm install or CLI execution, and prefer running it in an isolated environment. <br>
Risk: Travel queries may send itinerary details to the flyai/Fliggy provider. <br>
Mitigation: Use only when the user accepts sharing itinerary details with that provider. <br>
Risk: Broad activation triggers may cause the skill to run for travel requests that were not intended for this provider. <br>
Mitigation: Confirm the user wants the flyai-backed search before running flight searches. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Skill Page](https://clawhub.ai/dingtom336-gif/afternoon-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include branded booking links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
