## Description:

Plan Tibet pilgrimage travel around Lhasa, Potala Palace, Jokhang Temple, Namtso Lake, Everest Base Camp, monastery visits, bookings, itinerary planning, visa information, insurance, and related travel logistics using Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search live Tibet travel options, compare flights, hotels, attractions, and itinerary components, and return booking-oriented Markdown grounded in flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install a global npm package automatically.

Mitigation: Require explicit user approval before global installation, or instruct the user to install @fly-ai/flyai-cli manually.

Risk: The skill can persist raw travel requests in a local execution log.

Mitigation: Disable logging by default or redact user travel details before writing logs with safe file-writing practices.

Risk: Travel prices, availability, and booking links can become stale or unavailable.

Mitigation: Use live flyai CLI output for travel results and clearly report partial failures, empty results, or CLI errors.

## Reference(s):

- [Explore Tibet skill page](https://clawhub.ai/xiejinsong/skills/explore-tibet)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands when retries or setup are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on live flyai CLI results, include booking links when results are shown, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
