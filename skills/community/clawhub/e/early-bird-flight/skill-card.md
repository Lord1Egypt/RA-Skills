## Description: <br>
Book early bird flights with dawn departure and early morning deals, using flyai CLI results for live travel options and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search early morning flight options, compare routes, and present booking links from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may globally install and run an unpinned third-party travel CLI. <br>
Mitigation: Require explicit user approval before installation and prefer a pinned or sandboxed install of `@fly-ai/flyai-cli`. <br>
Risk: Flight-search details may be shared with the travel provider used by the CLI. <br>
Mitigation: Confirm the user is comfortable sharing the route, date, and related search details before running live searches. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
