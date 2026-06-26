## Description: <br>
Helps agents search UK flight options using flyai/Fliggy CLI output and return bookable results for routes involving London, Edinburgh, Manchester, and other UK destinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to collect flight-search parameters, run flyai searches, compare recommended, cheapest, fastest, direct, or flexible-date UK routes, and format bookable Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install a global third-party CLI when flyai is missing. <br>
Mitigation: Require explicit approval before any global npm install and prefer running the skill in an isolated environment. <br>
Risk: Travel wording is broader than the flight-search workflow supported by the artifact. <br>
Mitigation: Treat the skill as flight-search only unless separate evidence supports hotels, trains, attractions, insurance, or car rental behavior. <br>
Risk: Flight recommendations and booking links depend on live flyai output and may be unavailable or incomplete. <br>
Mitigation: Verify every result includes a detailUrl booking link, retry once on failures, and ask for alternate dates or routes when no valid results are returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/palexu/explore-uk) <br>
- [Parameter collection and output templates](artifact/references/templates.md) <br>
- [Scenario playbooks](artifact/references/playbooks.md) <br>
- [Failure recovery](artifact/references/fallbacks.md) <br>
- [Execution runbook](artifact/references/runbook.md) <br>
- [Node.js installation](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight-search summaries with comparison tables, booking links, and inline shell commands for flyai execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for results; each included flight result must contain a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
