## Description: <br>
Book Vietnam travel options, especially flights to Hanoi, Ho Chi Minh City, and Da Nang, by running the flyai CLI and formatting real-time results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning agents use this skill to collect flight search parameters, run the flyai CLI, and return concise Markdown flight options with booking links. It is intended for users comparing Vietnam routes, prices, durations, and direct-flight options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global third-party CLI package. <br>
Mitigation: Review the skill before installing, prefer manually installing or approving the flyai CLI, and use it only in environments where global npm packages are permitted. <br>
Risk: Flight search details and booking links are handled by flyai or its booking provider. <br>
Mitigation: Use the skill only when sharing itinerary details with that third-party service is acceptable, and treat booking links as third-party output. <br>


## Reference(s): <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; raw JSON is not returned to the user.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
