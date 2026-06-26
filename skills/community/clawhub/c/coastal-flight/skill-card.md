## Description: <br>
Searches coastal, seaside city, beach town, and harbor destination flights through the flyai/Fliggy CLI and formats real-time travel results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-assistant agents use this skill to collect flight search parameters, run real-time flyai coastal flight searches, and present bookable flight options for seaside and harbor destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation of a global npm package for the flyai CLI. <br>
Mitigation: Ask the user to approve package installation before running npm install, and continue only when the installed CLI can be verified. <br>
Risk: Raw travel queries and command history may be retained locally in an execution log. <br>
Mitigation: Confirm before writing the local execution log, and avoid collecting sensitive travel details beyond what the search requires. <br>
Risk: Automatic fallback behavior can substitute dates after invalid or past-date input. <br>
Mitigation: Confirm replacement travel dates with the user before executing searches that use substituted dates. <br>


## Reference(s): <br>
- [Coastal Flight skill listing](https://clawhub.ai/dingtom336-gif/coastal-flight) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands for execution or troubleshooting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for flight data; valid flight results are expected to include Book links derived from detailUrl.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
