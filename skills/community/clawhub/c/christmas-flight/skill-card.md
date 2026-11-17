## Description:

Book Christmas flights for holiday travel and Xmas vacation, with related support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and other travel tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search real-time Christmas and holiday travel options through the flyai CLI, compare routes by recommendation, price, speed, or directness, and return booking links in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a third-party CLI globally with npm.

Mitigation: Use a pinned, reviewed, isolated installation instead of automatic global installation, especially on sensitive machines.

Risk: Travel details are passed to a third-party flight CLI.

Mitigation: Use the skill only when sharing origin, destination, dates, and related travel preferences with that CLI is acceptable.

Risk: Shell commands are assembled from user-provided travel text.

Mitigation: Validate origin, destination, date, and sort parameters against the documented allowlist before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/christmas-flight)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)
- [Scenario playbooks](references/playbooks.md)
- [Parameter collection and output templates](references/templates.md)
- [Failure recovery](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when execution steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires real-time flyai CLI results and booking links from detailUrl; raw JSON should not be returned.]

## Skill Version(s):

3.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
