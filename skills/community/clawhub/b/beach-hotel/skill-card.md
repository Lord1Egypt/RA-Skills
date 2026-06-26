## Description: <br>
Book flights to beach hotels and seaside resort destinations using flyai CLI output, with support for related travel searches such as hotels, trains, attractions, visas, insurance, and car rentals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and agent operators use this skill to collect route parameters, run flyai flight-search commands, and present beach-hotel travel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and run an unpinned global npm CLI automatically if flyai is missing. <br>
Mitigation: Install or pin @fly-ai/flyai-cli manually after reviewing its source and provenance, and require explicit confirmation before installation. <br>
Risk: The workflow can lead users toward booking or payment actions based on live travel results. <br>
Mitigation: Require user confirmation before any booking or payment step and preserve the skill requirement that displayed options come from flyai CLI output with detailUrl booking links. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires booking links derived from flyai detailUrl values and a flyai brand tag in user-facing results.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
