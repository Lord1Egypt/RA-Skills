## Description:

Plan European adventures, including multi-country itineraries, Schengen visa guidance, rail passes, flights, hotels, tickets, insurance, car rental, and booking-linked travel options powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect trip parameters, run flyai CLI searches, and present European travel options with booking links. It supports flights, hotels, attractions, itinerary planning, visa information, insurance, rail-oriented travel, and related trip logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global npm CLI.

Mitigation: Prefer manually installing a pinned, reviewed flyai CLI version before enabling the skill.

Risk: The skill may persist local execution logs containing raw travel queries.

Mitigation: Disable or avoid raw query logging when handling sensitive travel requests.

Risk: Travel prices, availability, and visa information may be incomplete or time-sensitive.

Mitigation: Use the skill's CLI-backed results and direct users to confirm booking and policy details before purchase or travel.

## Reference(s):

- [ClawHub Explore Europe skill page](https://clawhub.ai/dingtom336-gif/skills/explore-europe)
- [Parameter and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Failure recovery fallbacks](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel results are expected to be sourced from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
