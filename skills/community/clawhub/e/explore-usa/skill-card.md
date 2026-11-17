## Description:

Plan American travel across New York, Los Angeles, San Francisco, national parks, Las Vegas, and coast-to-coast trips using flyai CLI results for flights, hotels, attractions, itineraries, visa information, insurance, car rental, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search flights, hotels, attractions, and USA itinerary options through flyai CLI results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global travel CLI.

Mitigation: Pin and review the flyai CLI version, avoid automatic global installation, and require explicit user approval before install or execution.

Risk: The skill includes an internal execution log pattern that can persist raw user travel queries.

Mitigation: Disable or redesign hidden logging so sensitive user queries are not persisted through shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-usa)
- [Parameter and output templates](references/templates.md)
- [USA travel playbooks](references/playbooks.md)
- [Failure recovery fallbacks](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with booking tables, booking links, concise travel guidance, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output for travel results; booking entries are expected to include detailUrl links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
