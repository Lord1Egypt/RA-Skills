## Description:

Book flights for gap year travel and year-off adventures. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search gap-year and long-term-trip travel options through the flyai CLI, then present concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a global third-party npm CLI.

Mitigation: Use a pinned and reviewed CLI version in a sandboxed environment, and require explicit user approval before installation or command execution.

Risk: Travel searches may be sent through the flyai/Fliggy workflow.

Mitigation: Confirm the user is comfortable sharing travel-search details with that workflow before running searches.

Risk: The booking-link workflow is rigid and may limit user control over result handling.

Mitigation: Review generated results before acting on links, and preserve user choice when filtering or presenting options.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/gap-year-travel)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results should be based on flyai CLI output, include a conclusion first, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
