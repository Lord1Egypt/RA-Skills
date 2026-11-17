## Description:

Book flights to Italy including Rome, Milan, and Florence, and support related travel tasks such as hotels, train tickets, attractions, itinerary planning, visa information, travel insurance, and car rental through flyai/Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search Italy flight options and related travel services from real-time flyai CLI output, then present concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned global CLI.

Mitigation: Review before installing, use an isolated environment, require explicit install consent, and pin and verify the CLI before execution.

Risk: The skill builds shell commands from user-provided travel parameters.

Mitigation: Validate all parameters before execution and avoid passing sensitive travel details unless the user accepts sharing them with the external flight service.

Risk: Booking links and travel data come from an external flight service.

Mitigation: Render only trusted booking links from CLI output and review results before relying on prices, availability, or itinerary details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-italy)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel results with inline booking links and flyai CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses real-time CLI output only; every listed travel result must include a booking link.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
