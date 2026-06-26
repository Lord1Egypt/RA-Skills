## Description: <br>
Book flights for holiday festivals, cultural events, and seasonal celebrations with flexible date ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search festival and holiday flight options from user-supplied routes, dates, and budget constraints through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install an unpinned global npm CLI. <br>
Mitigation: Require explicit user approval before any npm install and prefer a pinned or isolated install. <br>
Risk: Travel search details are sent to the flyai/Fliggy CLI. <br>
Mitigation: Use the skill only when that data sharing is acceptable for the user's travel request. <br>


## Reference(s): <br>
- [festival-flight release page](https://clawhub.ai/palexu/festival-flight) <br>
- [palexu publisher profile](https://clawhub.ai/user/palexu) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback procedures](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight options must be based on flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
