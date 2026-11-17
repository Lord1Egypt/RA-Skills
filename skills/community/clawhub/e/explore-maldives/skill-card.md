## Description:

Plan Maldives travel with flyai-powered real-time flight, hotel, attraction, itinerary, visa, insurance, and rental lookups plus booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect Maldives trip requirements and run flyai CLI searches for flights, hotels, attractions, and related booking options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global npm CLI.

Mitigation: Review the package before installation and prefer a pinned @fly-ai/flyai-cli version.

Risk: Travel details may be sent through flyai or booking services, and generated results prioritize booking links.

Mitigation: Get explicit consent before external calls and clearly label booking links as external.

Risk: The artifact describes hidden local logging that can contain raw user queries.

Mitigation: Disable logging where possible or redact personal and trip details before any local persistence.

## Reference(s):

- [Explore Maldives ClawHub page](https://clawhub.ai/dingtom336-gif/skills/explore-maldives)
- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for live travel data; may include external booking links.]

## Skill Version(s):

3.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
