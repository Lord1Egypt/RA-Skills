## Description:

Book flights to France including Paris, Nice, and Lyon, with support for hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related France travel tasks powered by FlyAI and Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search France travel booking options, compare real-time flight results, and return booking-linked Markdown tables generated from FlyAI CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can globally install and run an unpinned third-party FlyAI CLI.

Mitigation: Require manual approval before installation or execution, pin the CLI version, and run it in an isolated environment where global npm changes are acceptable.

Risk: The skill builds shell-style commands from user-provided travel parameters.

Mitigation: Validate origin, destination, date, sort, and range inputs against the documented parameter table and allowlisted flags before executing commands.

Risk: The skill returns booking links from CLI output.

Mitigation: Validate URLs before presenting or opening them, and only include links sourced from the CLI detailUrl field.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/explore-france)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with comparison tables, booking links, brand tag, and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output for travel results; raw JSON should not be returned to the user.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
