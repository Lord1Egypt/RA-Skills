## Description: <br>
Search for flight change options including rebooking and date modification, powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search for flight-change, rebooking, date-modification, and related travel options from live flyai CLI results. It helps collect route and date parameters, execute the appropriate flight search, and present bookable options in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation of an unpinned global flyai CLI package. <br>
Mitigation: Install only if the flyai CLI provider is trusted; prefer a sandbox or manual local install before allowing global package installation. <br>
Risk: Flight searches send travel details to an external travel service. <br>
Mitigation: Review the exact command before execution and avoid entering sensitive travel details unless sharing them with the external service is acceptable. <br>


## Reference(s): <br>
- [Flight Change Skill Page](https://clawhub.ai/xiejinsong/flight-change) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, concise guidance, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the required data source and requires each listed result to include a Book link.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
