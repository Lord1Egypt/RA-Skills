## Description: <br>
Plan Bali trips with real-time flyai CLI results for flights, hotels, attractions, itineraries, visa information, travel insurance, car rental, and booking links powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search Bali flights, lodging, attractions, and related travel services through flyai CLI commands, then present concise Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or require a global @fly-ai/flyai-cli package before use. <br>
Mitigation: Review the CLI package and installation policy before deployment; install it in a controlled environment when possible. <br>
Risk: The skill sends travel searches to the provider and can produce booking links based on those outbound requests. <br>
Mitigation: Avoid entering passport numbers, payment data, or highly sensitive trip details; review provider terms before booking. <br>
Risk: The runbook describes optional local persistence of raw execution requests in .flyai-execution-log.json. <br>
Mitigation: Disable, delete, or rotate local execution logs when raw request retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/explore-bali) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when troubleshooting is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel facts; successful result entries must include booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
