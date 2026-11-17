## Description:

Book flights to the Philippines including Manila, Boracay, and Cebu, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy and flyai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search Philippines-focused flights and related travel options from flyai CLI results, then present concise booking-oriented Markdown with comparison tables and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global third-party CLI.

Mitigation: Use an isolated environment, approve installation manually, and verify the package source before execution.

Risk: Travel search inputs may be sent to a third-party flight service.

Mitigation: Avoid entering unnecessary personal or sensitive information in search queries.

Risk: Booking links are taken from CLI output and may not be independently validated by the skill.

Mitigation: Verify booking domains and offer details before opening links or completing purchases.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/explore-philippines)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, concise travel guidance, and booking links derived from CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI execution for travel results; should not present booking options when CLI data is unavailable.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
