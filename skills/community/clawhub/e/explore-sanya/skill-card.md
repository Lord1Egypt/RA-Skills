## Description:

Explore Sanya helps agents plan Sanya travel with real-time flight, hotel, attraction, itinerary, and booking-link results through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search and compare Sanya flights, hotels, attractions, and trip options with current booking links. It is intended for Sanya and Hainan travel requests that require live travel data rather than static destination advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and use an unpinned third-party global travel CLI.

Mitigation: Pin and verify the flyai CLI package version before installation, and review CLI behavior before using it for live travel searches.

Risk: The skill may persist raw travel queries in a hidden local execution log.

Mitigation: Disable or remove the hidden execution log behavior before deployment, or avoid entering sensitive personal, payment, or itinerary details.

Risk: The skill produces booking links for live travel services.

Mitigation: Review returned booking links and pricing before acting, and avoid sharing highly sensitive personal or payment information through the agent workflow.

## Reference(s):

- [Explore Sanya skill page](https://clawhub.ai/dingtom336-gif/skills/explore-sanya)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when travel options are returned.]

## Skill Version(s):

3.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
