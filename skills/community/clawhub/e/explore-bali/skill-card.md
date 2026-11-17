## Description:

Plan your Bali dream trip - Ubud rice terraces, Seminyak beach clubs, Uluwatu temple sunsets, Nusa Penida cliffs, and spiritual yoga retreats; also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to plan Bali trips by collecting travel parameters, running flyai CLI searches for flights, hotels, attractions, and related services, and returning Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before running travel searches.

Mitigation: Install @fly-ai/flyai-cli manually from a reviewed, pinned version and verify flyai --version before use.

Risk: The skill may contact third-party travel services and produce booking links.

Mitigation: Review generated links and provider terms before booking; do not treat results as confirmed reservations until provider checkout is complete.

Risk: The skill can persist raw travel requests in a local execution log.

Mitigation: Disable or remove the execution log before using the skill with personal travel details.

## Reference(s):

- [Explore Bali ClawHub listing](https://clawhub.ai/dingtom336-gif/skills/explore-bali)
- [Templates SOP](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data; booking links use detailUrl when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
