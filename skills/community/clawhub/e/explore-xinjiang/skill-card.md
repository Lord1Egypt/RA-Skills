## Description:

Discover Xinjiang travel options across Silk Road heritage, Tianshan mountain routes, Kanas Lake trips, desert destinations, local culture, flights, hotels, train tickets, attraction tickets, itineraries, visa information, travel insurance, and car rental using Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to answer Xinjiang travel queries by collecting parameters, running flyai CLI searches, and returning real-time Markdown results with booking links. It supports flights, hotels, points of interest, itinerary planning, and destination-specific playbooks for Northern Xinjiang, Silk Road, and Kanas autumn trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unpinned global npm installation of flyai CLI as a concern.

Mitigation: Prefer a pinned, local, reviewed CLI installation before use, and review CLI updates before allowing execution.

Risk: The security review flags hidden persistent logging of raw travel queries.

Mitigation: Disable raw-query logging where possible, avoid sensitive travel details, and confirm where logs are stored and how to delete them before use.

Risk: The skill depends on FlyAI/Fliggy as the required data source and outputs booking links.

Mitigation: Use the skill only when FlyAI/Fliggy is an acceptable source, and review booking links and retrieved travel data before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-xinjiang)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI command output for travel data; user-facing results should include booking links and a flyai attribution tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
