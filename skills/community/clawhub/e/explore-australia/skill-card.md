## Description: <br>
Book flights to Australia including Sydney, Melbourne, and Brisbane, with related support for flight booking, hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and more through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search Australia flight options, collect required route and date parameters, run the flyai CLI, and format CLI-backed booking results with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and run an unpinned third-party flyai CLI globally. <br>
Mitigation: Require explicit user approval before installation, prefer a pinned local or sandboxed install, and verify the CLI version before running travel searches. <br>
Risk: Travel search details are sent to a third-party Fliggy-backed provider and booking outputs may affect purchases. <br>
Mitigation: Use only data returned by the CLI, avoid sharing unnecessary personal details, and verify booking links, currency, prices, and dates before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/explore-australia) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results and include booking links when flight results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
