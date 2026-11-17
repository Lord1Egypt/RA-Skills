## Description:

Plan Bali travel with real-time FlyAI/Fliggy-backed searches for flights, hotels, attractions, temples, beaches, villas, itineraries, and related travel services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel planners and agent users use this skill to collect Bali trip parameters, run FlyAI CLI searches, and present bookable Markdown comparisons for flights, lodging, attractions, and itinerary options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned global FlyAI CLI installation.

Mitigation: Use a pinned local or sandboxed CLI installation and review install commands before execution.

Risk: Travel searches may be processed by FlyAI/Fliggy and can reflect commercial booking-link bias.

Mitigation: Get explicit user consent before network-backed searches and present results as booking-provider data rather than neutral market coverage.

Risk: The workflow may persist raw travel queries in .flyai-execution-log.json.

Mitigation: Disable, redact, or periodically delete local query logs when they may contain personal travel details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/bali-travel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown comparison tables with booking links and inline shell commands for retry or setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results, include booking links from detailUrl values, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
