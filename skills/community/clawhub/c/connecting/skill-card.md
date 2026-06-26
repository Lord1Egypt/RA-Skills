## Description: <br>
Searches connecting flights, layover options, transit hubs, and multi-leg transfer routes using flyai CLI results powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agents use this skill to search connecting flights, compare layover routes, and format real-time booking options from flyai CLI output. It is intended for travel-planning workflows where results must come from live tool output rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install a global CLI automatically. <br>
Mitigation: Review before installing and prefer manually installing and verifying the flyai CLI. <br>
Risk: The skill may persist raw travel-query logs, which can include sensitive travel or identity details. <br>
Mitigation: Avoid sensitive travel or identity details unless logging is disabled or redacted. <br>
Risk: Via-city and fallback results may not enforce every routing constraint documented by the skill. <br>
Mitigation: Review routing details carefully before relying on via-city or fallback results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/connecting) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results and should include booking links when presenting flight options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
