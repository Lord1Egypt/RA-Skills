## Description:

Book flights for cycling trips and bike tours, with related support for hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and more, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to search current flight options for cycling trips and bike tours, then compare results with direct booking links. It can also guide related travel planning workflows that the FlyAI CLI supports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks agents to install and run an unpinned global third-party FlyAI npm CLI.

Mitigation: Review the npm package before use, prefer a pinned or local install, and require explicit approval before installation or execution.

Risk: The security summary says the skill forces travel results through one booking-link workflow.

Mitigation: Treat booking links as external commercial actions and require user confirmation before opening links or proceeding with booking.

## Reference(s):

- [Skill page](https://clawhub.ai/xiejinsong/skills/cycling-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables and inline booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
