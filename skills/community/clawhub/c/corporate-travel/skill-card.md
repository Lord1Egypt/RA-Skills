## Description: <br>
Book corporate travel flights for company trips and enterprise travel, with support for related travel booking tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and travel coordinators use this skill to search corporate flight options, compare recommended, cheapest, fastest, and direct routes, and return booking links from FlyAI CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external FlyAI npm CLI and may require a global npm installation before use. <br>
Mitigation: Install only after approving the FlyAI CLI dependency, and consider running it in a managed or sandboxed environment for corporate travel searches. <br>
Risk: Corporate travel search details may be shared with FlyAI or Fliggy through CLI execution. <br>
Mitigation: Use the skill only when sharing the route, date, and travel preference details with the external travel service is acceptable under company policy. <br>


## Reference(s): <br>
- [Corporate Travel skill page](https://clawhub.ai/xiejinsong/corporate-travel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
