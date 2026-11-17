## Description:

Searches for flight change options, including rebooking and date modification, and can route related travel searches through Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel support agents use this skill to collect route and date inputs, run flyai CLI flight-search commands, and format flight-change options with booking links and change-policy reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and execute an unpinned third-party flyai CLI globally.

Mitigation: Audit and install the CLI yourself, pin an approved version where possible, and require approval before execution.

Risk: Flight results and booking links depend on a third-party CLI and may direct users to mandatory booking links.

Mitigation: Verify prices, terms, and change policies directly with the airline or booking provider before acting.

Risk: The skill searches replacement flight options but does not prove that an existing ticket can be changed.

Mitigation: Treat output as search guidance and confirm any ticket modification through the airline or booking provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/flight-change)
- [Parameter collection and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Failure recovery](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must be sourced from flyai CLI output and include Book links when flight options are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
