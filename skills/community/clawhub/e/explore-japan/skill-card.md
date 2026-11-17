## Description:

Your complete Japan travel companion for flights, hotels, attractions, itinerary planning, visa information, travel insurance, car rental, and related Japan travel guidance powered by Fliggy and flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to retrieve Japan travel options from flyai CLI and present flights, lodging, attractions, itinerary guidance, visa information, and booking links in user-facing Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unpinned global flyai CLI installation requirement.

Mitigation: Use a pinned, reviewed, isolated installation path and avoid automatic global npm installation.

Risk: The security evidence reports hidden raw-query execution logging.

Mitigation: Disable or remove the hidden log, or redact raw user input and define clear retention controls.

Risk: Travel queries and booking actions may be shared with the flyai service and provider-specific booking links.

Mitigation: Use the skill only when users are comfortable sharing travel queries with that service and verify booking details with the provider before purchase.

## Reference(s):

- [Explore Japan ClawHub Listing](https://clawhub.ai/dingtom336-gif/skills/explore-japan)
- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)
- [Parent flyai Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results and should include provider booking links when results are shown.]

## Skill Version(s):

3.2.1 (source: ClawHub release metadata; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
