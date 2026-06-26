## Description: <br>
Find romantic hotels for couples with king-size beds, scenic views, intimate atmosphere, and couple amenities such as champagne and spa packages, powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for romantic hotel stays, collect destination and date parameters, run flyai hotel-search commands, and return booking-ready Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global flyai CLI dependency before use. <br>
Mitigation: Require manual approval for npm install commands and prefer an isolated environment before running the skill. <br>
Risk: The skill can persist raw travel queries and plans in .flyai-execution-log.json. <br>
Mitigation: Disable or delete the log file after use and avoid entering sensitive travel details unless needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/couple-romantic-stay) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for travel data and booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
