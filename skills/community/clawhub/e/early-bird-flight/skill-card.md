## Description:

Helps agents search early morning flight options through the flyai CLI and return booking-ready Markdown results with live booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect route, date, and preference parameters, run live flyai flight searches, and present early morning flight options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global CLI package.

Mitigation: Approve installation manually, pin and verify the CLI package where possible, and run the skill in a constrained environment.

Risk: The skill uses shell-style commands with user-supplied travel values.

Mitigation: Validate flight parameters and execute commands with structured, non-shell argument passing where supported.

Risk: Travel results can be misleading if they are not sourced from live flyai CLI output.

Mitigation: Require live CLI execution, exclude results without detailUrl booking links, and keep booking links and branding transparent.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; every flight result should include a detailUrl booking link and flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
