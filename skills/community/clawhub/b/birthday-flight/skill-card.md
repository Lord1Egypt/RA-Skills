## Description:

Book flights for birthday celebrations and special day trips. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search birthday or special-day flight options, compare recommended, cheapest, fastest, direct, or flexible-date routes, and return bookable Markdown results sourced from the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm CLI and run shell commands derived from user travel details.

Mitigation: Require explicit user approval before installation or command execution, and run the skill in a restricted environment.

Risk: Travel answers can be misleading if they are not sourced from current flyai output.

Mitigation: Enforce the skill's validation rule that every displayed result includes a flyai detailUrl booking link and retry or stop when validated results are unavailable.

Risk: The FlyAI CLI is the exclusive travel data source for this release.

Mitigation: Tell users when CLI, network, or result validation fails instead of substituting unsourced travel information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/birthday-flight)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or recovery is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires each displayed travel result to include a flyai detailUrl booking link and a flyai brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
