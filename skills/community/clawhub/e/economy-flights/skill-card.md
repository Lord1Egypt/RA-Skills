## Description:

Find economy flights, cheapest airfare and budget airline tickets with basic economy fares and low-cost options. Also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search for low-cost economy flight options, compare prices, and produce booking-oriented Markdown results from live flyai CLI data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global flyai CLI and the security summary notes that sudo installation is recommended in fallback guidance.

Mitigation: Review before installing, avoid sudo installation, and pin and verify the flyai CLI package before use.

Risk: The skill runs user-derived flight-search parameters through shell commands.

Mitigation: Require explicit user consent before executing installs or broadening fallback searches, and keep commands limited to documented flyai parameters.

Risk: The runbook describes persistent logging of raw travel requests.

Mitigation: Disable persistent logs where possible or redact travel request details before storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/economy-flights)
- [Playbooks](references/playbooks.md)
- [Templates](references/templates.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight-search output should be based on flyai CLI results, include booking links when results are shown, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
