## Description: <br>
Search for flights with airport lounge access and premium terminal options, plus related travel booking tasks such as hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and agents use this skill to search flight options with lounge or premium terminal preferences, collect required route parameters, execute flyai CLI searches, and present bookable Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and run an unpinned global npm CLI when flyai is missing. <br>
Mitigation: Require explicit user approval before installation, prefer a pinned @fly-ai/flyai-cli version, and document how to uninstall or replace the global package. <br>
Risk: Travel search details are sent to the flyai provider when CLI searches are executed. <br>
Mitigation: Use the skill only when the user is comfortable sharing route, date, and preference details with that provider. <br>
Risk: Incorrect or fabricated travel results could mislead users if the CLI is skipped or returns invalid data. <br>
Mitigation: Enforce the skill's requirement that every presented result comes from flyai CLI output and includes a detailUrl booking link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/airport-lounge) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or troubleshooting is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output, include booking links from detailUrl, avoid raw JSON, and follow the user's language.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
