## Description: <br>
Book flights for anniversary celebrations and milestone occasions using flyai CLI results powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-booking agents use this skill to collect route, date, and cabin preferences, run flyai flight searches, and present anniversary-ready flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the flyai CLI globally with npm and run external searches. <br>
Mitigation: Approve installation manually, prefer sandboxed or project-local installation, and pin or review the package version before use. <br>
Risk: Route, date, and cabin preferences are sent to the flyai/Fliggy provider during searches. <br>
Mitigation: Use the skill only when sharing travel search details with that provider is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/anniversary-flight) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, inline booking links, and occasional bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight options must be sourced from flyai CLI output and include detailUrl booking links when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
