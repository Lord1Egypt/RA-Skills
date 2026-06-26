## Description: <br>
Finds economy flights and low-cost airfare by guiding an agent to run the flyai CLI and format live results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search for economy flight options, collect route, date, and budget parameters, execute flyai searches, and present bookable low-fare results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global npm CLI. <br>
Mitigation: Require explicit user confirmation before installing @fly-ai/flyai-cli globally, and provide the manual install command if automated installation fails. <br>
Risk: Travel search details may be sent to flyai/Fliggy. <br>
Mitigation: Tell users before execution that route, date, and budget details may be sent to the travel provider, and avoid collecting passport numbers or other sensitive personal details. <br>
Risk: Fallback searches may broaden dates, airports, or budget assumptions. <br>
Mitigation: Confirm broader searches with the user before expanding beyond the requested route, dates, or price constraints. <br>
Risk: Execution logs may persist raw user queries locally. <br>
Mitigation: Avoid writing local logs unless the user consents, and delete or disable .flyai-execution-log.json when logs are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/economy-flights) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Economy flight playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown flight summaries and comparison tables with inline shell commands and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live flyai CLI output, includes [Book](detailUrl) links for flight results, and avoids raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
